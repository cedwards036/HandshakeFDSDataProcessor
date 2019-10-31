import unittest

from src.survey_data_model.survey_response.location import Location


class TestLocation(unittest.TestCase):

    def assert_full_loc(self, expected: str, location: Location):
        self.assertEqual(expected, location.full_location)

    def test_null_location(self):
        self.assert_full_loc('', Location())

    def test_passing_empty_string_counts_as_null(self):
        self.assertEqual(Location(), Location(city='', state='', country=''))
        self.assertEqual(Location(city='Hong Kong'), Location(city='Hong Kong', state='', country=''))

    def test_full_location_is_set_given_only_one_location_field(self):
        self.assert_full_loc('Baltimore', Location(city='Baltimore'))
        self.assert_full_loc('Maryland', Location(state='Maryland'))
        self.assert_full_loc('United States', Location(country='United States'))

    def test_full_location_is_set_given_two_location_fields(self):
        self.assert_full_loc('Baltimore, Maryland', Location(city='Baltimore', state='Maryland'))
        self.assert_full_loc('Baltimore, United States', Location(city='Baltimore', country='United States'))
        self.assert_full_loc('Maryland, United States', Location(state='Maryland', country='United States'))

    def test_full_location_is_set_given_all_three_fields(self):
        self.assert_full_loc('Baltimore, Maryland, United States', Location(city='Baltimore', state='Maryland', country='United States'))

    def test_full_location_responds_to_field_updates(self):
        location = Location(city='Baltimore', state='Maryland', country='United States')
        self.assert_full_loc('Baltimore, Maryland, United States', location)
        location.city = 'London'
        self.assert_full_loc('London, Maryland, United States', location)
        location.state = 'England'
        location.country = 'United Kingdom'
        self.assert_full_loc('London, England, United Kingdom', location)

    def test_to_dict(self):
        self.assertEqual({'city': 'Baltimore', 'state': 'Maryland', 'country': 'United States'},
                         Location(city='Baltimore', state='Maryland', country='United States').to_dict())
