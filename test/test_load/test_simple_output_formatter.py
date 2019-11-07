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
        formatted_responses = SimpleOutputFormatter().format(response)
        self.assertEqual(1, len(formatted_responses))
        self.assertEqual('Folsom', formatted_responses[0]['city'])
        self.assertEqual('California', formatted_responses[0]['state'])
        self.assertEqual('United States', formatted_responses[0]['country'])
        with self.assertRaises(KeyError):
            formatted_responses[0]['location']

    def test_removes_degree_field(self):
        formatted_responses = SimpleOutputFormatter().format(SurveyResponse())
        with self.assertRaises(KeyError):
            formatted_responses[0]['jhu_degrees']

    def test_flattens_degree_fields_given_no_degrees(self):
        formatted_responses = SimpleOutputFormatter().format(SurveyResponse())
        self.assertIsNone(formatted_responses[0]['jhu_majors'])
        self.assertIsNone(formatted_responses[0]['jhu_colleges'])

    def test_flattens_single_degree(self):
        response = SurveyResponse()
        response.student.jhu_degrees = [JHUDegree(degree='B.S.', major='Comp Sci', college='WSE')]
        formatted_responses = SimpleOutputFormatter().format(response)
        self.assertEqual('B.S.: Comp Sci', formatted_responses[0]['jhu_majors'])
        self.assertEqual('WSE', formatted_responses[0]['jhu_colleges'])

    def test_flattens_multiple_degrees_with_same_college_and_degree(self):
        response = SurveyResponse()
        response.student.jhu_degrees = [JHUDegree(degree='B.S.', major='Mech E', college='WSE'),
                                        JHUDegree(degree='B.S.', major='Comp Sci', college='WSE')]
        formatted_responses = SimpleOutputFormatter().format(response)
        self.assertEqual('B.S.: Comp Sci; B.S.: Mech E', formatted_responses[0]['jhu_majors'])
        self.assertEqual('WSE', formatted_responses[0]['jhu_colleges'])

    def test_flattens_multiple_degrees_with_different_college_and_degree(self):
        response = SurveyResponse()
        response.student.jhu_degrees = [JHUDegree(degree='B.A.', major='English', college='KSAS'),
                                        JHUDegree(degree='B.S.', major='Comp Sci', college='WSE')]
        formatted_responses = SimpleOutputFormatter().format(response)
        self.assertEqual('B.A.: English; B.S.: Comp Sci', formatted_responses[0]['jhu_majors'])
        self.assertEqual('KSAS; WSE', formatted_responses[0]['jhu_colleges'])
