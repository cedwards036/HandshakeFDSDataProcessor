import unittest

from src.load.simple_output_formatter import SimpleOutputFormatter
from src.survey_data_model import SurveyResponse


class TestSimpleOutputFormatter(unittest.TestCase):

    def test_formatter_flattens_location_data(self):
        response = SurveyResponse()
        response.metadata.location.city = 'Folsom'
        response.metadata.location.state = 'California'
        response.metadata.location.country = 'United States'
        formatted_response = SimpleOutputFormatter().format(response)
        self.assertEqual('Folsom', formatted_response['city'])
        self.assertEqual('California', formatted_response['state'])
        self.assertEqual('United States', formatted_response['country'])
        with self.assertRaises(KeyError):
            formatted_response['location']
