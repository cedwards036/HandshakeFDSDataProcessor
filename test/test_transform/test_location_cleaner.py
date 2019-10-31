import unittest

from src.survey_data_model.survey_response.location import Location
from src.transform.location_cleaner import LocationCleaner


class TestLocationCleaner(unittest.TestCase):

    def test_location_cleaner(self):
        cleaner = LocationCleaner()
        cleaned_location = Location('New York City', 'New York', 'United States')
        cleaner.add_mapping('New York, New York', cleaned_location)
        unclean_location = Location('New York', 'New York')
        self.assertEqual(cleaned_location, cleaner.get_mapping(unclean_location))


if __name__ == '__main__':
    unittest.main()
