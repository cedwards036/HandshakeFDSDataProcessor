import unittest

from src.survey_data_model import FDS2018CustomQuestions
from src.survey_data_model.survey_response.custom_questions import ActivityQuestionSet


class TestActivityQuestionSet(unittest.TestCase):

    def test_all_count_updates_automatically(self):
        test_activity_set = ActivityQuestionSet()
        self.assertIsNone(test_activity_set.all_count)
        test_activity_set.unpaid_count = 2
        self.assertEqual(2, test_activity_set.all_count)
        test_activity_set.paid_count = 3
        self.assertEqual(5, test_activity_set.all_count)
        test_activity_set.unpaid_count = 10
        self.assertEqual(13, test_activity_set.all_count)

    def test_all_count_stays_none_if_a_count_is_set_to_none(self):
        test_activity_set = ActivityQuestionSet()
        test_activity_set.unpaid_count = None
        self.assertIsNone(test_activity_set.all_count)


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
