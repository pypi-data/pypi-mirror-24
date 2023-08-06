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

""""""
import os
import unittest
from mailbox import mbox
from tempfile import TemporaryDirectory

from mailman.app.lifecycle import create_list
from mailman.testing.helpers import specialized_message_from_string as mfs

from mailman_pgp.archivers.local_mbox import LocalMailboxArchiver
from mailman_pgp.config import config
from mailman_pgp.database import mm_transaction
from mailman_pgp.model.list import PGPMailingList
from mailman_pgp.pgp.mime import MIMEWrapper
from mailman_pgp.testing.layers import PGPConfigLayer
from mailman_pgp.testing.pgp import load_key


class TestPGPMboxArchiver(unittest.TestCase):
    layer = PGPConfigLayer

    def setUp(self):
        self.msg = mfs("""\
To: test@example.com
From: anne@example.com
Subject: Testing the test list
Message-ID: <ant>
Message-ID-Hash: MS6QLWERIJLGCRF44J7USBFDELMNT2BW

Tests are better than no tests
but the water deserves to be swum.
""")
        with mm_transaction():
            self.mlist = create_list('test@example.com',
                                     style_name='pgp-default')
        self.pgp_list = PGPMailingList.for_list(self.mlist)
        self.list_key = load_key('ecc_p256.priv.asc')
        self.pgp_list.key = self.list_key

    def test_no_links(self):
        self.assertIsNone(LocalMailboxArchiver.list_url(self.mlist))
        self.assertIsNone(LocalMailboxArchiver.permalink(self.mlist, self.msg))

    def test_no_pgp_list(self):
        with mm_transaction():
            ordinary = create_list('ordinary@example.com')

            LocalMailboxArchiver.archive_message(ordinary, self.msg)

    def test_archives(self):
        with TemporaryDirectory() as mailbox_dir:
            config.set('archiving', 'mailbox_dir', mailbox_dir)
            LocalMailboxArchiver.archive_message(self.mlist, self.msg)

            list_dir = os.path.join(mailbox_dir, self.mlist.fqdn_listname)

            mailbox = mbox(list_dir)
            messages = mailbox.values()
            self.assertEqual(len(messages), 1)

            message = messages[0]
            wrapped = MIMEWrapper(message)
            self.assertTrue(wrapped.is_encrypted())
            decrypted = wrapped.decrypt(self.list_key)
            self.assertTrue(self.msg.as_string(), decrypted.as_string())
