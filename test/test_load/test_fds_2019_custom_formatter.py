import unittest

from src.load.custom_formatters import FDS2019CustomFormatter


class TestFDS2019CustomFormatter(unittest.TestCase):

    def test_flattens_activity_questions(self):
        test_data = {'internships': {'name': 'internships', 'unpaid_count': 0, 'paid_count': 2, 'all_count': 2,
                                     'gained_valuable_skills': 'Strongly Agree', 'connected_with_mentor': 'Somewhat Agree',
                                     'may_lead_to_future_opps': 'Strongly Agree', 'gained_clarity': 'Strongly Agree'},
                     'research': {'name': 'research', 'unpaid_count': 1, 'paid_count': 4, 'all_count': 5,
                                  'gained_valuable_skills': 'Strongly Disagree', 'connected_with_mentor': 'Somewhat Disagree',
                                  'may_lead_to_future_opps': 'Neutral', 'gained_clarity': 'Agree'},
                     'other_field': 'value'}
        expected = {'internships_unpaid_count': 0, 'internships_paid_count': 2, 'internships_all_count': 2,
                    'internships_gained_valuable_skills': 'Strongly Agree', 'internships_connected_with_mentor': 'Somewhat Agree',
                    'internships_may_lead_to_future_opps': 'Strongly Agree', 'internships_gained_clarity': 'Strongly Agree',
                    'research_unpaid_count': 1, 'research_paid_count': 4, 'research_all_count': 5,
                    'research_gained_valuable_skills': 'Strongly Disagree', 'research_connected_with_mentor': 'Somewhat Disagree',
                    'research_may_lead_to_future_opps': 'Neutral', 'research_gained_clarity': 'Agree',
                    'other_field': 'value'}
        formatter = FDS2019CustomFormatter()
        self.assertEqual(expected, formatter.format(test_data))
