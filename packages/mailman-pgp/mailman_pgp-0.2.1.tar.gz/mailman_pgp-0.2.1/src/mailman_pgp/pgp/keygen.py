# Copyright (C) 2017 Jan Jancar
#
# This file is a part of the Mailman PGP plugin.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""List key generator runs in a separate process to not block for the
potentially long key generation operation."""

import multiprocessing as mp

from flufl.lock import Lock
from pgpy import PGPKey, PGPUID
from pgpy.constants import (
    CompressionAlgorithm, HashAlgorithm, KeyFlags, SymmetricKeyAlgorithm)

from mailman_pgp.config import config
from mailman_pgp.utils.pgp import key_from_file


class ListKeyGenerator(mp.Process):
    """A multiprocessing list key generator."""

    def __init__(self, pgp_list):
        super().__init__(
                target=self._run,
                args=(config.pgp.primary_key_args, config.pgp.sub_key_args,
                      pgp_list.mlist.display_name,
                      pgp_list.mlist.posting_address,
                      pgp_list.mlist.request_address,
                      pgp_list.key_path),
                daemon=True)
        self._pgp_list = pgp_list

    def generate(self, block=False):
        self.start()
        if block:
            self.join()
            return key_from_file(self._pgp_list.key_path)

    def _run(self, primary_args, subkey_args, display_name, posting_address,
             request_address, key_path):
        """
        Generate the list keypair and save it.

        :param primary_args:
        :param subkey_args:
        :param display_name:
        :param posting_address:
        :param request_address:
        :param key_path:
        """
        self.key = self._create(primary_args, subkey_args, display_name,
                                posting_address,
                                request_address)
        with Lock(key_path + '.lock'):
            self._save(self.key, key_path)

    def _create(self, primary_args, subkey_args, display_name, posting_address,
                request_address):
        """
        Generate the list `PGPKey` keypair, with posting and request UIDs.

        Use a Sign+Certify main key and Encrypt subkey.
        :param primary_args:
        :param subkey_args:
        :param display_name:
        :param posting_address:
        :param request_address:
        :return: `PGPKey`
        """
        common_params = dict(
                hashes=[HashAlgorithm.SHA256,
                        HashAlgorithm.SHA384,
                        HashAlgorithm.SHA512,
                        HashAlgorithm.SHA224],
                ciphers=[SymmetricKeyAlgorithm.AES256,
                         SymmetricKeyAlgorithm.AES192,
                         SymmetricKeyAlgorithm.AES128],
                compression=[CompressionAlgorithm.ZLIB,
                             CompressionAlgorithm.BZ2,
                             CompressionAlgorithm.ZIP,
                             CompressionAlgorithm.Uncompressed]
        )

        # Generate the Sign + Certify primary key.
        key = PGPKey.new(*primary_args)
        key_params = dict(usage={KeyFlags.Sign, KeyFlags.Certify},
                          **common_params)
        # Generate the posting + request uids.
        main_uid = PGPUID.new(display_name, email=posting_address)
        request_uid = PGPUID.new(display_name,
                                 email=request_address)
        # Generate the Encrypt subkey.
        subkey = PGPKey.new(*subkey_args)
        subkey_params = dict(
                usage={KeyFlags.EncryptCommunications,
                       KeyFlags.EncryptStorage},
                **common_params
        )
        # Put it all together.
        key.add_uid(main_uid, primary=True, **key_params)
        key.add_uid(request_uid, **key_params)
        key.add_subkey(subkey, **subkey_params)
        return key

    def _save(self, key, key_path):
        """
        Save the generated key.

        :param key:
        :param key_path:
        """
        try:
            with open(key_path, 'w') as key_file:
                key_file.write(str(key))
        except FileNotFoundError:
            # Just eat it up.
            pass
