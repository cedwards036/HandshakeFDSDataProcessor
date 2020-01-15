import unittest

from src.survey_data_model import Location
from src.transform.value_map import ValueMap, ValueMapBuilder


class TestBuildValueMap(unittest.TestCase):

    def test_build_empty_value_map(self):
        self.assertEqual(ValueMap(), ValueMapBuilder.build_value_map([], 'from_field', 'to_field'))

    def test_build_single_value_mapping(self):
        value_map = ValueMapBuilder.build_value_map([{'first_field': 'value1', 'second_field': 'value2'}],
                                    'first_field', 'second_field')
        self.assertEqual('value2', value_map.get_mapping('value1'))

    def test_build_multiple_value_mapping(self):
        value_map = ValueMapBuilder.build_cached_value_map([{'unclean': 'Valv', 'clean': 'Valve'},
                                                            {'unclean': 'deLOIte', 'clean': 'Deloitte'},
                                                            {'unclean': 'Goggle', 'clean': 'Google'}],
                                    'unclean', 'clean')
        self.assertEqual('Valve', value_map.get_mapping('Valv'))
        self.assertEqual('Deloitte', value_map.get_mapping('deLOIte'))
        self.assertEqual('Google', value_map.get_mapping('Goggle'))

    def assert_mapping_is(self, expected: Location, unclean_location: Location, loc_map):
        self.assertEqual(expected.to_dict(), loc_map.get_mapping(unclean_location).to_dict())

    def test_build_mapping_for_empty_location(self):
        test_input = [{'raw_location': '$8jg$gjfi', 'city': '', 'state': '', 'country': ''}]
        location_map = ValueMapBuilder.build_cached_location_map(test_input, 'raw_location')
        self.assert_mapping_is(Location(), Location('$8jg$gjfi'), location_map)

    def test_build_mapping_for_multiple_locations(self):
        test_input = [{'raw_location': 'Folsom', 'city': 'Folsom', 'state': 'California', 'country': 'United States'},
                      {'raw_location': 'New York, New York', 'city': 'New York City', 'state': 'New York', 'country': 'United States'},
                      {'raw_location': 'Beijing, China', 'city': 'Beijing', 'state': '', 'country': 'China'}]
        location_map = ValueMapBuilder.build_cached_location_map(test_input, 'raw_location')
        self.assert_mapping_is(Location('Folsom', 'California', 'United States'), Location('Folsom'), location_map)
        self.assert_mapping_is(Location('New York City', 'New York', 'United States'), Location('New York, New York'), location_map)
        self.assert_mapping_is(Location('Beijing', None, 'China'), Location('Beijing', 'China'), location_map)

    def test_build_multi_field_value_map(self):
        value_map = ValueMapBuilder.build_multi_field_value_map([{'first_field': 'value1', 'second_field': 'value2', 'third_field': 'value3'}],
                                                                'first_field', {'second_field', 'third_field'})
        self.assertEqual({'second_field': 'value2', 'third_field': 'value3'}, value_map.get_mapping('value1'))
