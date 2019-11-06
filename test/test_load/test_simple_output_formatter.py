import unittest

from src.load.simple_output_formatter import SimpleOutputFormatter
from src.survey_data_model import JHUDegree
from src.survey_data_model import SurveyResponse


class TestSimpleOutputFormatter(unittest.TestCase):

    def test_flattens_location_data(self):
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

    def test_flattens_degree_fields_given_no_degrees(self):
        formatted_response = SimpleOutputFormatter().format(SurveyResponse())
        self.assertIsNone(formatted_response['jhu_degrees'])
        self.assertIsNone(formatted_response['jhu_majors'])
        self.assertIsNone(formatted_response['jhu_colleges'])

    def test_flattens_single_degree(self):
        response = SurveyResponse()
        response.student.jhu_degrees = [JHUDegree(degree='B.S.', major='Comp Sci', college='WSE')]
        formatted_response = SimpleOutputFormatter().format(response)
        self.assertEqual('B.S.', formatted_response['jhu_degrees'])
        self.assertEqual('Comp Sci', formatted_response['jhu_majors'])
        self.assertEqual('WSE', formatted_response['jhu_colleges'])

    def test_flattens_multiple_degrees_with_same_college_and_degree(self):
        response = SurveyResponse()
        response.student.jhu_degrees = [JHUDegree(degree='B.S.', major='Mech E', college='WSE'),
                                        JHUDegree(degree='B.S.', major='Comp Sci', college='WSE')]
        formatted_response = SimpleOutputFormatter().format(response)
        self.assertEqual('B.S.', formatted_response['jhu_degrees'])
        self.assertEqual('Comp Sci; Mech E', formatted_response['jhu_majors'])
        self.assertEqual('WSE', formatted_response['jhu_colleges'])

    def test_flattens_multiple_degrees_with_different_college_and_degree(self):
        response = SurveyResponse()
        response.student.jhu_degrees = [JHUDegree(degree='B.A.', major='English', college='KSAS'),
                                        JHUDegree(degree='B.S.', major='Comp Sci', college='WSE')]
        formatted_response = SimpleOutputFormatter().format(response)
        self.assertEqual('B.A.; B.S.', formatted_response['jhu_degrees'])
        self.assertEqual('Comp Sci; English', formatted_response['jhu_majors'])
        self.assertEqual('KSAS; WSE', formatted_response['jhu_colleges'])
