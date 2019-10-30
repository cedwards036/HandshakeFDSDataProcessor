import unittest

from src.survey_data_model import SurveyResponse
from src.survey_data_model.response_dataset import ResponseDataset


class TestResponseDataset(unittest.TestCase):

    def test_look_up_response_by_username(self):
        test_dataset = ResponseDataset()
        test_response = SurveyResponse()
        test_response.student.username = 'AJG3T9'
        test_dataset.add_response(test_response)
        self.assertEqual(test_response, test_dataset.get_response_by_username('AJG3T9'))

    def test_look_up_response_by_username_throws_exception_when_given_invalid_username(self):
        test_dataset = ResponseDataset()
        with self.assertRaises(ResponseDataset.InvalidUsernameException):
            test_dataset.get_response_by_username('Invalid Username')
