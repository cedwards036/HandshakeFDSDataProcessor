import unittest

from src.survey_data_model.survey_response.location import Location
from src.transform.location_map import build_location_map


class TestLocationMapBuilder(unittest.TestCase):

    def assert_mapping_is(self, expected: Location, unclean_location: Location, loc_map):
        self.assertEqual(expected.to_dict(), loc_map.get_mapping(unclean_location).to_dict())

    def test_build_mapping_for_empty_location(self):
        test_input = [{'raw_location': '$8jg$gjfi', 'city': '', 'state': '', 'country': ''}]
        location_map = build_location_map(test_input)
        self.assert_mapping_is(Location(), Location('$8jg$gjfi'), location_map)

    def test_build_mapping_for_multiple_locations(self):
        test_input = [{'raw_location': 'Folsom', 'city': 'Folsom', 'state': 'California', 'country': 'United States'},
                      {'raw_location': 'New York, New York', 'city': 'New York City', 'state': 'New York', 'country': 'United States'},
                      {'raw_location': 'Beijing, China', 'city': 'Beijing', 'state': '', 'country': 'China'}]
        location_map = build_location_map(test_input)
        self.assert_mapping_is(Location('Folsom', 'California', 'United States'), Location('Folsom'), location_map)
        self.assert_mapping_is(Location('New York City', 'New York', 'United States'), Location('New York, New York'), location_map)
        self.assert_mapping_is(Location('Beijing', None, 'China'), Location('Beijing', 'China'), location_map)
