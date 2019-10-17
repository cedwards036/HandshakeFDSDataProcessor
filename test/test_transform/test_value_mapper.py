import unittest

from src.transform.value_mapper import ValueMapping


class TestValueReplacer(unittest.TestCase):

    def test_replaces_known_value(self):
        replacer = ValueMapping()
        replacer.add_mapping('NYC', 'New York')
        self.assertEqual('New York', replacer.get_mapping('NYC'))

    def test_throws_exception_if_value_is_not_known(self):
        replacer = ValueMapping()
        with self.assertRaises(ValueMapping.NoKnownMappingException):
            replacer.get_mapping('some unknown value')
