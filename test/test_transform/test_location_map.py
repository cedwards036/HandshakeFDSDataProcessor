import unittest

from src.survey_data_model.survey_response.location import Location
from src.transform.location_map import LocationMap


class TestLocationCleaner(unittest.TestCase):

    def test_location_map(self):
        loc_map = LocationMap()
        cleaned_location = Location('New York City', 'New York', 'United States')
        loc_map.add_mapping('New York, New York', cleaned_location)
        unclean_location = Location('New York', 'New York')
        self.assertEqual(cleaned_location, loc_map.get_mapping(unclean_location))

    def test_location_map_returns_a_value_if_value_is_already_clean(self):
        loc_map = LocationMap()
        cleaned_location = Location('New York City', 'New York', 'United States')
        loc_map.add_mapping('New York, New York', cleaned_location)
        self.assertEqual(cleaned_location, loc_map.get_mapping(cleaned_location))

if __name__ == '__main__':
    unittest.main()
