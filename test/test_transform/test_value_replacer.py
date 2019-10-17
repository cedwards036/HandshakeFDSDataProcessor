import unittest

from src.transform.value_replacer import ValueReplacer


class TestValueReplacer(unittest.TestCase):

    def test_replaces_known_value(self):
        replacer = ValueReplacer()
        replacer.add_mapping('NYC', 'New York')
        self.assertEqual('New York', replacer.replace('NYC'))

    def test_throws_exception_if_value_is_not_known(self):
        replacer = ValueReplacer()
        with self.assertRaises(ValueReplacer.NoKnownMappingException):
            replacer.replace('some unknown value')
