import unittest

from src.transform.is_jhu import is_jhu


class TestIsJHU(unittest.TestCase):

    def test_none_is_not_jhu(self):
        self.assertFalse(is_jhu(None))

    def test_empty_str_is_not_jhu(self):
        self.assertFalse(is_jhu(''))

    def test_simple_hopkins_str_is_jhu(self):
        self.assertTrue(is_jhu('Johns Hopkins'))

    def test_compound_hopkins_str_is_jhu(self):
        self.assertTrue(is_jhu('The johns hopkins Hospital'))

    def test_complex_hopkins_str_is_jhu(self):
        self.assertTrue(is_jhu('   !!!! The johnS   hOPKINS AP   L     '))
