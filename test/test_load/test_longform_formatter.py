import unittest

from src.load.longform_formatter import LongformFormatter
from src.survey_data_model import JHUDegree
from src.survey_data_model import SurveyResponse


class TestLongformFormatter(unittest.TestCase):

    def test_flattens_location_data(self):
        response = SurveyResponse()
        response.student.jhu_degrees = [JHUDegree(degree='B.S.', major='Comp Sci', college='WSE')]
        response.metadata.location.city = 'Folsom'
        response.metadata.location.state = 'California'
        response.metadata.location.country = 'United States'
        formatted_responses = LongformFormatter().format(response)
        self.assertEqual('Folsom', formatted_responses[0]['city'])
        self.assertEqual('California', formatted_responses[0]['state'])
        self.assertEqual('United States', formatted_responses[0]['country'])
        with self.assertRaises(KeyError):
            formatted_responses[0]['location']

    def test_produces_one_row_given_no_jhu_degree(self):
        response = SurveyResponse()
        formatted_responses = LongformFormatter().format(response)
        self.assertEqual(1, len(formatted_responses))
        self.assertIsNone(formatted_responses[0]['jhu_degree'])
        self.assertIsNone(formatted_responses[0]['jhu_major'])
        self.assertIsNone(formatted_responses[0]['jhu_college'])

    def test_produces_one_row_given_one_jhu_degree(self):
        response = SurveyResponse()
        response.student.jhu_degrees = [JHUDegree(degree='B.S.', major='Comp Sci', college='WSE')]
        formatted_responses = LongformFormatter().format(response)
        self.assertEqual(1, len(formatted_responses))
        self.assertEqual('B.S.', formatted_responses[0]['jhu_degree'])
        self.assertEqual('Comp Sci', formatted_responses[0]['jhu_major'])
        self.assertEqual('WSE', formatted_responses[0]['jhu_college'])

    def test_produces_multiple_rows_given_multiple_jhu_degrees(self):
        response = SurveyResponse()
        response.student.jhu_degrees = [JHUDegree(degree='B.S.', major='Comp Sci', college='WSE'),
                                        JHUDegree(degree='B.A.', major='English', college='KSAS'),
                                        JHUDegree(degree='M.B.A.', major='Business', college='Carey')]
        formatted_responses = LongformFormatter().format(response)
        self.assertEqual(3, len(formatted_responses))
        self.assertEqual('B.S.', formatted_responses[0]['jhu_degree'])
        self.assertEqual('Comp Sci', formatted_responses[0]['jhu_major'])
        self.assertEqual('WSE', formatted_responses[0]['jhu_college'])
        self.assertEqual('B.A.', formatted_responses[1]['jhu_degree'])
        self.assertEqual('English', formatted_responses[1]['jhu_major'])
        self.assertEqual('KSAS', formatted_responses[1]['jhu_college'])
        self.assertEqual('M.B.A.', formatted_responses[2]['jhu_degree'])
        self.assertEqual('Business', formatted_responses[2]['jhu_major'])
        self.assertEqual('Carey', formatted_responses[2]['jhu_college'])

    def test_jhu_degrees_field_is_not_present_after_formatting(self):
        response = SurveyResponse()
        formatted_responses = LongformFormatter().format(response)
        self.assertTrue('jhu_degrees' not in formatted_responses[0])
