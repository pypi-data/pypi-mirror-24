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


import unittest

from mailman_pgp.config import mm_config
from mailman_pgp.plugin import PGPMailman
from mailman_pgp.testing.layers import PGPConfigLayer


class TestPlugin(unittest.TestCase):
    layer = PGPConfigLayer

    def test_instance_loaded(self):
        self.assertIn('pgp', mm_config.plugins.keys())
        instance = mm_config.plugins['pgp']
        self.assertIsInstance(instance, PGPMailman)
