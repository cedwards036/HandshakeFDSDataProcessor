import os
import unittest
from datetime import datetime

from src.extract.custom_parsers import FDS2018CustomParser
from src.extract.extract_responses import extract_raw_responses, ResponseParser

FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_input_data.csv')


class TestExtractResponses(unittest.TestCase):

    def setUp(self):
        self.fds_2018_parser = FDS2018CustomParser()
        self.test_response_1 = {
            'Id': '659754',
            'Username': 'astudent1',
            'Auth Identifier': 'astudent1@johnshopkins.edu',
            'Card ID': '6.01E+15',
            'Name': 'Arthur Student',
            'School Email': 'astudent1@jhu.edu',
            'Personal Email': 'cool_dude_42@gmail.com',
            'Recipient Primary Major': 'Chemical & Biomolecular Eng',
            'Recipient Secondary Majors': '',
            'Recipient Graduation Date': '5/1/2018',
            'Recipient Education Level': 'Bachelors',
            'Recipient Primary College': 'Whiting School of Engineering',
            'Recipient Gender': '',
            'Recipient Ethnicity': '',
            'Recipient Visa Status': 'U.S. Citizen',
            'Recipient Veteran Status': '',
            'Recipient First Generation': '',
            'Recipient Athlete Status': '',
            'Recipient Hometown': '',
            'Recipient Graduation Group Name': '18-May',
            'Response Primary Major': 'Chemical & Biomolecular Eng',
            'Response Secondary Majors': '',
            'Response Education Level': 'Bachelors',
            'Response Graduation Date': '5/1/2018',
            'Response Primary College': '',
            'Response Status': 'submitted',
            'Response Date': '',
            'Outcome': 'Still Looking',
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
            'Not Seeking Option': '',
            'Location': '',
            'Offer Date': '',
            'Accept Date': '',
            'Start Date': '',
            'Salary': '',
            'Bonus Amount': '',
            'Other Compensation': '',
            'Authorized to work in US?': '',
            'Submitted By': 'Arthur Student',
            'Knowledge Response?': '',
            'Knowledge Source': 'Survey Response',
            'At the time you accepted your current position, did you accept it with the intention that it would only be a temporary, “gap year” position, before applying to graduate or professional school in the next year or two?': '',
            'During your time at Hopkins, how many *unpaid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*. ': '0',
            'During your time at Hopkins, how many *paid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*.': '0',
            'During your time at Hopkins, how many unique *unpaid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': '0',
            'During your time at Hopkins, how many unique *paid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': '0'
        }
        self.test_response_2 = {
            'Id': '659755',
            'Username': 'bstudent2',
            'Auth Identifier': 'bstudent2@johnshopkins.edu',
            'Card ID': '6.01E+15',
            'Name': 'Benjamin Student',
            'School Email': 'bstudent2@jhu.edu',
            'Personal Email': 'ok_dude_41@gmail.com',
            'Recipient Primary Major': 'Global Environmental Change and Sustainability',
            'Recipient Secondary Majors': 'Earth & Planetary Sciences',
            'Recipient Graduation Date': '5/1/2018',
            'Recipient Education Level': 'Bachelors',
            'Recipient Primary College': 'Krieger School of Arts & Sciences',
            'Recipient Gender': '',
            'Recipient Ethnicity': '',
            'Recipient Visa Status': 'U.S. Citizen',
            'Recipient Veteran Status': '',
            'Recipient First Generation': '',
            'Recipient Athlete Status': '',
            'Recipient Hometown': '',
            'Recipient Graduation Group Name': '18-May',
            'Response Primary Major': 'Global Environmental Change and Sustainability',
            'Response Secondary Majors': '',
            'Response Education Level': 'Bachelors',
            'Response Graduation Date': '5/1/2018',
            'Response Primary College': '',
            'Response Status': 'submitted',
            'Response Date': '2019-01-31 19:52:48 UTC',
            'Outcome': 'Working',
            'Employer Name': 'Coro',
            'Employer Industry': '',
            'Employment Category': 'Fellowship',
            'Employment Type': 'Full-Time',
            'Job Function': '',
            'Job Position': 'Coro Fellow',
            'Found through Handshake': '',
            'Employed During Education': '',
            'Internship': '',
            'Continuing Education School': 'Harvard',
            'Continuing Education Level': 'Masters',
            'Continuing Education Major': 'English Literature',
            'Is Fellowship?': 'Yes',
            'Fellowship Name': 'Coro Fellowship',
            'Military Branch': '',
            'Military Rank': '',
            'Specialization': '',
            'Still Looking Option': '',
            'Not Seeking Option': '',
            'Location': 'Pittsburgh, Pennsylvania, United States of America',
            'Offer Date': '',
            'Accept Date': '',
            'Start Date': '',
            'Salary': '',
            'Bonus Amount': '',
            'Other Compensation': '',
            'Authorized to work in US?': '',
            'Submitted By': 'James Staffmember',
            'Knowledge Response?': 'Yes',
            'Knowledge Source': 'LinkedIn',
            'At the time you accepted your current position, did you accept it with the intention that it would only be a temporary, “gap year” position, before applying to graduate or professional school in the next year or two?': 'Yes',
            'During your time at Hopkins, how many *unpaid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*. ': '2',
            'During your time at Hopkins, how many *paid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*.': '0',
            'During your time at Hopkins, how many unique *unpaid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': '1',
            'During your time at Hopkins, how many unique *paid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': '0'
        }
        self.test_response_3 = {
            'Id': '659756',
            'Username': 'cstudent3',
            'Auth Identifier': 'cstudent3@johnshopkins.edu',
            'Card ID': '6.01E+15',
            'Name': 'Chelsea Student',
            'School Email': 'cstudent3@jhu.edu',
            'Personal Email': 'awesome_gal_99@gmail.com',
            'Recipient Primary Major': 'Public Health Studies',
            'Recipient Secondary Majors': '',
            'Recipient Graduation Date': '5/1/2018',
            'Recipient Education Level': 'Bachelors',
            'Recipient Primary College': 'Krieger School of Arts & Sciences',
            'Recipient Gender': '',
            'Recipient Ethnicity': '',
            'Recipient Visa Status': 'U.S. Citizen',
            'Recipient Veteran Status': '',
            'Recipient First Generation': '',
            'Recipient Athlete Status': '',
            'Recipient Hometown': '',
            'Recipient Graduation Group Name': '18-May',
            'Response Primary Major': 'Bachelors: Public Health Studies',
            'Response Secondary Majors': '',
            'Response Education Level': 'Bachelors',
            'Response Graduation Date': '5/1/2018',
            'Response Primary College': '',
            'Response Status': 'submitted',
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
            'Internship': '',
            'Continuing Education School': '',
            'Continuing Education Level': '',
            'Continuing Education Major': '',
            'Is Fellowship?': '',
            'Fellowship Name': '',
            'Military Branch': '',
            'Military Rank': '',
            'Specialization': '',
            'Still Looking Option': '',
            'Not Seeking Option': '',
            'Location': 'Washington, District of Columbia, United States',
            'Offer Date': '4/20/2017',
            'Accept Date': '4/28/2017',
            'Start Date': '5/25/2017',
            'Salary': '27560',
            'Bonus Amount': '0',
            'Other Compensation': '0',
            'Authorized to work in US?': 'TRUE',
            'Submitted By': 'Chelsea Student',
            'Knowledge Response?': '',
            'Knowledge Source': 'Survey Response',
            'At the time you accepted your current position, did you accept it with the intention that it would only be a temporary, “gap year” position, before applying to graduate or professional school in the next year or two?': 'Yes',
            'During your time at Hopkins, how many *unpaid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*. ': '3',
            'During your time at Hopkins, how many *paid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*.': '1',
            'During your time at Hopkins, how many unique *unpaid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': '0',
            'During your time at Hopkins, how many unique *paid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.': '2'
        }

    def test_extract_responses(self):
        self.assertEqual(3, len(extract_raw_responses(FILEPATH)))

    def test_date_fields_are_parsed_into_datetime_objects(self):
        response = ResponseParser(self.test_response_3).parse()
        self.assertEqual(datetime(2018, 10, 5, 14, 30, 6), response.response_datetime_utc)
        self.assertEqual(datetime(2017, 4, 20), response.employment.offer_date)
        self.assertEqual(datetime(2017, 4, 28), response.employment.accept_date)
        self.assertEqual(datetime(2017, 5, 25), response.employment.start_date)

    def test_empty_date_fields_are_parsed_into_none(self):
        response = ResponseParser(self.test_response_1).parse()
        self.assertIsNone(response.response_datetime_utc)
        self.assertIsNone(response.employment.offer_date)
        self.assertIsNone(response.employment.accept_date)
        self.assertIsNone(response.employment.start_date)

    def test_parser_parses_employment_fields_correctly(self):
        response = ResponseParser(self.test_response_3).parse()
        self.assertEqual('ScribeAmerica', response.employment.employer_name)
        self.assertEqual('Healthcare', response.employment.employer_industry)
        self.assertEqual('Organization', response.employment.employment_category)
        self.assertEqual('Full-Time', response.employment.employment_type)
        self.assertEqual('Healthcare Services', response.employment.job_function)
        self.assertEqual('Medical Scribe', response.employment.job_title)
        self.assertEqual(True, response.employment.found_through_handshake)
        self.assertEqual(False, response.employment.employed_during_education)
        self.assertEqual(27560, response.employment.salary)
        self.assertEqual(0, response.employment.bonus_amount)
        self.assertEqual(0, response.employment.other_compensation)
        self.assertIsNone(response.employment.is_internship)

    def test_parser_parses_education_fields_correctly(self):
        response = ResponseParser(self.test_response_2).parse()
        self.assertEqual('Harvard', response.cont_ed.school)
        self.assertEqual('Masters', response.cont_ed.level)
        self.assertEqual('English Literature', response.cont_ed.major)

    def test_2018_parser_parses_custom_questions_correctly(self):
        response = ResponseParser(self.test_response_3, self.fds_2018_parser).parse()
        self.assertEqual(True, response.custom.is_gap_year)
        self.assertEqual(3, response.custom.unpaid_internships_count)
        self.assertEqual(1, response.custom.paid_internships_count)
        self.assertEqual(4, response.custom.all_internships_count)
        self.assertEqual(0, response.custom.unpaid_research_count)
        self.assertEqual(2, response.custom.paid_research_count)
        self.assertEqual(2, response.custom.all_research_count)
