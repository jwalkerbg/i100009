# test_core_module_b.py

import unittest
from pgedit import core

class TestcoreB(unittest.TestCase):
    def test_hello_from_core_module_b(self):
        self.assertEqual(core.hello_from_core_module_b(),2)

    def test_goodbye_from_core_module_b(self):
        self.assertEqual(core.goodbye_from_core_module_b(),-2)