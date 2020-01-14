import unittest

from src.survey_data_model import Location
from src.transform.value_map import ValueMap, CachedValueMap


class TestValueMap(unittest.TestCase):

    def test_replaces_known_value(self):
        value_map = ValueMap()
        value_map.add_mapping('NYC', 'New York')
        self.assertEqual('New York', value_map.get_mapping('NYC'))

    def test_throws_exception_if_value_is_not_known(self):
        value_map = ValueMap()
        with self.assertRaises(ValueMap.NoKnownMappingException):
            value_map.get_mapping('some unknown value')

    def test_raises_error_if_given_already_clean_value_that_is_not_explicitly_mapped(self):
        value_map = ValueMap()
        value_map.add_mapping('NYC', 'New York')
        with self.assertRaises(ValueMap.NoKnownMappingException):
            self.assertEqual('New York', value_map.get_mapping('New York'))


class TestCachedValueMap(unittest.TestCase):

    def test_automatically_maps_none_to_none(self):
        value_map = CachedValueMap()
        self.assertIsNone(value_map.get_mapping(None))

    def test_just_returns_a_value_if_value_is_already_clean(self):
        value_map = CachedValueMap()
        value_map.add_mapping('NYC', 'New York')
        self.assertEqual('New York', value_map.get_mapping('New York'))


class TestLocationMap(unittest.TestCase):

    def test_location_map(self):
        loc_map = CachedValueMap(lambda loc: loc.full_location)
        cleaned_location = Location('New York City', 'New York', 'United States')
        loc_map.add_mapping('New York, New York', cleaned_location)
        unclean_location = Location('New York', 'New York')
        self.assertEqual(cleaned_location, loc_map.get_mapping(unclean_location))

    def test_location_map_returns_a_value_if_value_is_already_clean(self):
        loc_map = CachedValueMap(lambda loc: loc.full_location)
        cleaned_location = Location('New York City', 'New York', 'United States')
        loc_map.add_mapping('New York, New York', cleaned_location)
        self.assertEqual(cleaned_location, loc_map.get_mapping(cleaned_location))
