import unittest

from src.transform.value_map import ValueMap
from src.transform.value_map.build_value_map import build_value_map


class TestBuildValueMap(unittest.TestCase):

    def test_build_empty_value_map(self):
        self.assertEqual(ValueMap(), build_value_map([], 'from_field', 'to_field'))

    def test_build_single_value_mapping(self):
        value_map = build_value_map([{'first_field': 'value1', 'second_field': 'value2'}],
                                    'first_field', 'second_field')
        self.assertEqual('value2', value_map.get_mapping('value1'))

    def test_build_multiple_value_mapping(self):
        value_map = build_value_map([{'unclean': 'Valv', 'clean': 'Valve'},
                                     {'unclean': 'deLOIte', 'clean': 'Deloitte'},
                                     {'unclean': 'Goggle', 'clean': 'Google'}],
                                    'unclean', 'clean')
        self.assertEqual('Valve', value_map.get_mapping('Valv'))
        self.assertEqual('Deloitte', value_map.get_mapping('deLOIte'))
        self.assertEqual('Google', value_map.get_mapping('Goggle'))
