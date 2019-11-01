import os
import unittest
from datetime import datetime

from src.extract.custom_parsers import FDS2018CustomParser, FDS2019CustomParser, CustomParser, NullCustomParser
from src.extract.response_extractor import ResponseExtractor
from src.extract.response_parser import ResponseParser
from src.extract.value_parser import JHEDParser, LocationParser
from src.survey_data_model import SurveyResponse
from src.survey_data_model.survey_response.location import Location

TEST_RESPONSE_DATA_FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_response_data.csv')
TEST_DUPLICATE_FIELDS_FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_duplicate_fields.csv')


def make_response(fields: dict, custom_parser: CustomParser = NullCustomParser()) -> SurveyResponse:
    raw_response = {
        'Id': '',
        'Username': '',
        'Auth Identifier': '',
        'Card ID': '',
        'Name': '',
        'School Email': '',
        'Personal Email': '',
        'Recipient Primary Major': '',
        'Recipient Secondary Majors': '',
        'Recipient Graduation Date': '',
        'Recipient Education Level': '',
        'Recipient Primary College': '',
        'Recipient Gender': '',
        'Recipient Ethnicity': '',
        'Recipient Visa Status': '',
        'Recipient Veteran Status': '',
        'Recipient First Generation': '',
        'Recipient Athlete Status': '',
        'Recipient Hometown': '',
        'Recipient Graduation Group Name': '',
        'Response Primary Major': '',
        'Response Secondary Majors': '',
        'Response Education Level': '',
        'Response Graduation Date': '',
        'Response Primary College': '',
        'Response Status': '',
        'Response Date': '',
        'Outcome': '',
        'Employer Name': '',
        'Employer Industry': '',
        'Employment Category': '',
        'Employment Type': '',
        'Job Function': '',
        'Job Position': '',
        'Found through Handshake': '',
        'Employed During Education': '',
        'Internship': '',
        'Continuing Education School': '',
        'Continuing Education Level': '',
        'Continuing Education Major': '',
        'Is Fellowship?': '',
        'Fellowship Name': '',
        'Military Branch': '',
        'Military Rank': '',
        'Specialization': '',
        'Still Looking Option': 'Employment',
        'Not Seeking Option': 'Just Cause',
        'Location': '',
        'Offer Date': '',
        'Accept Date': '',
        'Start Date': '',
        'Annual Salary': '',
        'Bonus Amount': '',
        'Other Compensation': '',
        'Authorized to work in US?': '',
        'Submitted By': '',
        'Knowledge Response?': '',
        'Knowledge Source': '',
    }
    for field in fields:
        raw_response[field] = fields[field]
    return ResponseParser(raw_response, custom_parser).parse()


class TestExtractResponses(unittest.TestCase):

    def test_extract_recodes_duplicated_field_names(self):
        expected = [{
            'field_a': 'A      ',
            'field_b': 'B      ',
            'field_b_1': 'B1     ',
            'field_c': 'C      ',
            'field_c_1': 'C1     ',
            'field_c_2': 'C2',
            'field_d': ''
        }]
        self.assertEqual(expected, ResponseExtractor(TEST_DUPLICATE_FIELDS_FILEPATH).extract())


class TestResponseParser(unittest.TestCase):

    def setUp(self):
        self.fds_2018_parser = FDS2018CustomParser()
        self.continuing_education_response = make_response({
            'Continuing Education School': 'Harvard',
            'Continuing Education Level': 'Masters',
            'Continuing Education Major': 'English Literature',
        })
        self.working_response = make_response({
            'Id': '659756',
            'Username': 'HYU4IP',
            'Auth Identifier': 'cstudent3@johnshopkins.edu',
            'Name': 'Chelsea Student',
            'School Email': 'cstudent3@jhu.edu',
            'Personal Email': 'awesome_gal_99@gmail.com',
            'Recipient Graduation Date': '5/1/2018',
            'Recipient Education Level': 'Bachelors',
            'Response Date': '2018-10-05 14:30:06 UTC',
            'Outcome': 'Working',
            'Employer Name': 'ScribeAmerica',
            'Employer Industry': 'Healthcare',
            'Employment Category': 'Organization',
            'Employment Type': 'Full-Time',
            'Job Function': 'Healthcare Services',
            'Job Position': 'Medical Scribe',
            'Found through Handshake': 'Yes',
            'Employed During Education': 'No',
            'Location': 'Washington, District of Columbia, United States',
            'Offer Date': '4/20/2017',
            'Accept Date': '4/28/2017',
            'Start Date': '5/25/2017',
            'Annual Salary': '27560.56',
            'Bonus Amount': '0',
            'Other Compensation': '0',
            'Submitted By': 'Chelsea Student',
            'Knowledge Response?': 'Yes',
            'Knowledge Source': 'Survey Response'
        })

    def test_date_fields_are_parsed_into_datetime_objects(self):
        self.assertEqual(datetime(2018, 10, 5, 14, 30, 6), self.working_response.metadata.response_datetime_utc)
        self.assertEqual(datetime(2017, 4, 20), self.working_response.employment.offer_date)
        self.assertEqual(datetime(2017, 4, 28), self.working_response.employment.accept_date)
        self.assertEqual(datetime(2017, 5, 25), self.working_response.employment.start_date)

    def test_empty_date_fields_are_parsed_into_none(self):
        empty_response = make_response({})
        self.assertIsNone(empty_response.metadata.response_datetime_utc)
        self.assertIsNone(empty_response.employment.offer_date)
        self.assertIsNone(empty_response.employment.accept_date)
        self.assertIsNone(empty_response.employment.start_date)

    def test_parser_parses_employment_fields_correctly(self):
        self.assertEqual('ScribeAmerica', self.working_response.employment.employer_name)
        self.assertEqual('Healthcare', self.working_response.employment.employer_industry)
        self.assertEqual('Organization', self.working_response.employment.employment_category)
        self.assertEqual('Full-Time', self.working_response.employment.employment_type)
        self.assertEqual('Healthcare Services', self.working_response.employment.job_function)
        self.assertEqual('Medical Scribe', self.working_response.employment.job_title)
        self.assertEqual(True, self.working_response.employment.found_through_handshake)
        self.assertEqual(False, self.working_response.employment.employed_during_education)
        self.assertEqual(27560.56, self.working_response.employment.salary)
        self.assertEqual(0, self.working_response.employment.bonus_amount)
        self.assertEqual(0, self.working_response.employment.other_compensation)
        self.assertIsNone(self.working_response.employment.is_internship)

    def test_parser_parses_education_fields_correctly(self):
        self.assertEqual('Harvard', self.continuing_education_response.cont_ed.school)
        self.assertEqual('Masters', self.continuing_education_response.cont_ed.level)
        self.assertEqual('English Literature', self.continuing_education_response.cont_ed.major)

    def test_parser_parses_student_fields_correctly(self):
        self.assertEqual('HYU4IP', self.working_response.student.username)
        self.assertEqual('cstudent3@jhu.edu', self.working_response.student.email)
        self.assertEqual('cstudent3', self.working_response.student.jhed)
        self.assertEqual('Chelsea Student', self.working_response.student.full_name)

    def test_parser_parses_metadata_correctly(self):
        self.assertEqual('659756', self.working_response.metadata.response_id)
        self.assertEqual(datetime(2018, 10, 5, 14, 30, 6), self.working_response.metadata.response_datetime_utc)
        self.assertEqual('Working', self.working_response.metadata.outcome)
        self.assertEqual('Washington, District of Columbia, United States', self.working_response.metadata.location.full_location)
        self.assertEqual('Chelsea Student', self.working_response.metadata.submitted_by)
        self.assertEqual(True, self.working_response.metadata.is_knowledge_response)
        self.assertEqual('Survey Response', self.working_response.metadata.knowledge_source)

    def test_parser_parses_other_outcomes_fields_correctly(self):
        self.assertEqual('Employment', self.working_response.other_outcomes.still_looking_option)
        self.assertEqual('Just Cause', self.working_response.other_outcomes.not_seeking_option)


class TestParsingFellowshipResponses(unittest.TestCase):

    def setUp(self) -> None:
        self.employment_response = make_response({'Is Fellowship?': 'Yes', 'Outcome': 'Working', 'Employer Name': 'Coro'})
        self.cont_ed_response = make_response({'Is Fellowship?': 'Yes', 'Outcome': 'Continuing Education',
                                               'Continuing Education School': 'Norwegian University of Science and Technology',
                                               'Fellowship Name': 'Fulbright'})

    def test_parser_recodes_employment_fellowship_outcome(self):
        self.assertEqual('Fellowship', self.employment_response.metadata.outcome)

    def test_parser_recodes_cont_ed_fellowship_outcome(self):
        self.assertEqual('Fellowship', self.cont_ed_response.metadata.outcome)

    def test_parser_recodes_employer_as_fellowship_org(self):
        self.assertEqual('Coro', self.employment_response.fellowship_data.fellowship_org)

    def test_parser_recodes_cont_ed_school_as_fellowship_org(self):
        self.assertEqual('Norwegian University of Science and Technology', self.cont_ed_response.fellowship_data.fellowship_org)

    def test_parser_parses_fellowship_name(self):
        self.assertEqual('Fulbright', self.cont_ed_response.fellowship_data.fellowship_name)


class TestParsingMilitaryResponses(unittest.TestCase):

    def setUp(self) -> None:
        self.military_response = make_response({
            'Outcome': 'Military',
            'Military Branch': 'Army',
            'Military Rank': 'Officer',
            'Specialization': 'Civil Engineering'
        })

    def test_military_branch_becomes_employer_name(self):
        self.assertEqual('Army', self.military_response.employment.employer_name)

    def test_rank_and_specialization_become_job_title(self):
        self.assertEqual('Civil Engineering Officer', self.military_response.employment.job_title)

    def test_rank_and_specialization_null_combinations(self):
        null_rank_response = make_response({'Outcome': 'Military', 'Specialization': 'Civil Engineering'})
        self.assertEqual('Civil Engineering Specialist', null_rank_response.employment.job_title)
        null_specialization_response = make_response({'Outcome': 'Military', 'Military Rank': 'Officer'})
        self.assertEqual('Officer', null_specialization_response.employment.job_title)
        null_response = make_response({'Outcome': 'Military'})
        self.assertIsNone(null_response.employment.job_title)

    def test_employment_type_is_full_time(self):
        self.assertEqual('Full-Time', self.military_response.employment.employment_type)


class TestJHEDParser(unittest.TestCase):

    def test_throws_exception_on_non_jhed_str(self):
        with self.assertRaises(JHEDParser.UnexpectedValueException):
            JHEDParser('some random str').parse()

    def test_parses_jhed_from_auth_id(self):
        self.assertEqual('cstudent3', JHEDParser('cstudent3@johnshopkins.edu').parse())

    def test_parses_jhed_from_plain_jhed(self):
        self.assertEqual('cstudent3', JHEDParser('cstudent3').parse())


class TestLocationParser(unittest.TestCase):

    def assert_location_parsed_into(self, expected: Location, input_str: str):
        self.assertEqual(expected.to_dict(), LocationParser(input_str).parse().to_dict())

    def test_parses_empty_str_into_empty_location(self):
        self.assert_location_parsed_into(Location(), '')

    def test_parses_commaless_string_into_city_field(self):
        self.assert_location_parsed_into(Location(city='Baltimore'), 'Baltimore')
        self.assert_location_parsed_into(Location(city='Some - complex ##58$ str'), 'Some - complex ##58$ str')

    def test_trims_input(self):
        self.assert_location_parsed_into(Location(city='Baltimore'), '     Baltimore ')

    def test_parses_single_comma_string_into_city_and_state(self):
        self.assert_location_parsed_into(Location(city='Baltimore', state='United States'), ' Baltimore,  United States ')

    def test_parses_two_comma_string_into_full_location(self):
        self.assert_location_parsed_into(Location(city='Baltimore', state='Maryland', country='United States'), ' Baltimore,  Maryland,United States ')

    def test_parses_everything_after_the_second_comma_into_country(self):
        self.assert_location_parsed_into(Location(city='Baltimore', state='Maryland', country='United States, Earth, The Universe'), ' Baltimore,  Maryland,United States , Earth,The Universe ')


class Test2018ExtraQuestionsParser(unittest.TestCase):

    def test_2018_parser_parses_custom_questions_correctly(self):
        response = make_response({
            'At the time you accepted your current position, did you accept it with the intention that it would only be a temporary, “gap year” position, before applying to graduate or professional school in the next year or two?': 'Yes',
            'During your time at Hopkins, how many *unpaid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*. ': '3',
            'During your time at Hopkins, how many *paid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*.': '1',
            'During your time at Hopkins, how many unique *unpaid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': '0',
            'During your time at Hopkins, how many unique *paid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': '2'
        }, FDS2018CustomParser())
        self.assertEqual(True, response.custom.is_gap_year)
        self.assertEqual(3, response.custom.unpaid_internships_count)
        self.assertEqual(1, response.custom.paid_internships_count)
        self.assertEqual(4, response.custom.all_internships_count)
        self.assertEqual(0, response.custom.unpaid_research_count)
        self.assertEqual(2, response.custom.paid_research_count)
        self.assertEqual(2, response.custom.all_research_count)


class Test2019ExtraQuestionsParser(unittest.TestCase):

    def setUp(self) -> None:
        self.response = make_response({
            'At the time you accepted your current position, did you accept it with the intention that it would only be a temporary, “gap year” position, before applying to graduate or professional school in the next year or two?': 'No',
            'Did you participate in an internship during your time at Hopkins? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*.': 'Yes',
            'During your time at Hopkins, how many *unpaid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*.': '3',
            'During your time at Hopkins, how many *paid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*.': '7',
            'I gained valuable skills': 'Somewhat Agree',
            'I connected with a mentor': 'Strongly Disagree',
            'This internship may lead to future opportunities': 'Strongly Agree',
            'I gained clarity about what I find meaningful': '',
            'Did you participate in research during your time at Hopkins? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': 'No',
            'During your time at Hopkins, how many unique *unpaid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': '2',
            'During your time at Hopkins, how many unique *paid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': '1',
            'I gained valuable skills_1': 'Strongly Agree',
            'I connected with a mentor_1': 'Neither Agree nor Disagree',
            'This research experience may lead to future opportunities': 'Strongly Disagree',
            'I gained clarity about what I find meaningful_1': '',
            'I gained clarity about what I find meaningful_2': 'Somewhat Agree',
        }, FDS2019CustomParser())

    def test_counts_are_parsed_correctly(self):
        self.assertEqual(3, self.response.custom.internships.unpaid_count)
        self.assertEqual(7, self.response.custom.internships.paid_count)
        self.assertEqual(10, self.response.custom.internships.all_count)
        self.assertEqual(2, self.response.custom.research.unpaid_count)
        self.assertEqual(1, self.response.custom.research.paid_count)
        self.assertEqual(3, self.response.custom.research.all_count)

    def test_gap_year_questions_is_parsed_correctly(self):
        self.assertEqual(False, self.response.custom.is_gap_year)

    def test_internship_satisfaction_questions(self):
        self.assertEqual('Somewhat Agree', self.response.custom.internships.gained_valuable_skills)
        self.assertEqual('Strongly Disagree', self.response.custom.internships.connected_with_mentor)
        self.assertEqual('Strongly Agree', self.response.custom.internships.may_lead_to_future_opps)
        self.assertIsNone(self.response.custom.internships.gained_clarity)

    def test_research_satisfaction_questions(self):
        self.assertEqual('Strongly Agree', self.response.custom.research.gained_valuable_skills)
        self.assertEqual('Neither Agree nor Disagree', self.response.custom.research.connected_with_mentor)
        self.assertEqual('Strongly Disagree', self.response.custom.research.may_lead_to_future_opps)
        self.assertEqual('Somewhat Agree', self.response.custom.research.gained_clarity)
