import unittest

from src.transform.value_map import ValueMap


class TestValueReplacer(unittest.TestCase):

    def test_replaces_known_value(self):
        replacer = ValueMap()
        replacer.add_mapping('NYC', 'New York')
        self.assertEqual('New York', replacer.get_mapping('NYC'))

    def test_just_returns_a_value_if_value_is_already_clean(self):
        replacer = ValueMap()
        replacer.add_mapping('NYC', 'New York')
        self.assertEqual('New York', replacer.get_mapping('New York'))

    def test_throws_exception_if_value_is_not_known(self):
        replacer = ValueMap()
        with self.assertRaises(ValueMap.NoKnownMappingException):
            replacer.get_mapping('some unknown value')
