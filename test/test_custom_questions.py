import unittest

from src.survey_response import FDS2018CustomQuestions


class Test2018CustomQuestions(unittest.TestCase):

    def test_all_internships_count_updates_automatically(self):
        test_response = FDS2018CustomQuestions()
        self.assertIsNone(test_response.all_internships_count)
        test_response.unpaid_internships_count = 2
        self.assertEqual(2, test_response.all_internships_count)
        test_response.paid_internships_count = 3
        self.assertEqual(5, test_response.all_internships_count)
        test_response.unpaid_internships_count = 10
        self.assertEqual(13, test_response.all_internships_count)

    def test_all_research_count_updates_automatically(self):
        test_response = FDS2018CustomQuestions()
        self.assertIsNone(test_response.all_research_count)
        test_response.unpaid_research_count = 2
        self.assertEqual(2, test_response.all_research_count)
        test_response.paid_research_count = 3
        self.assertEqual(5, test_response.all_research_count)
        test_response.unpaid_research_count = 10
        self.assertEqual(13, test_response.all_research_count)
