from typing import List

from src.extract.custom_parsers import CustomParser, NullCustomParser
from src.extract.file_utils import read_csv
from src.extract.value_parser import (StringParser, DateParser, DatetimeParser,
                                      YesNoParser, IntParser, JHEDParser)
from src.survey_response import SurveyResponse


def extract_raw_responses(filepath: str) -> List[dict]:
    return read_csv(filepath)


class ResponseParser:

    def __init__(self, raw_data: dict, custom_questions_parser: CustomParser = NullCustomParser()):
        self._raw_data = raw_data
        self._response = SurveyResponse(custom_questions_parser.get_questions_class())
        self._custom_parser = custom_questions_parser

    def parse(self) -> SurveyResponse:
        self._parse_student_fields()
        self._parse_employment_fields()
        self._parse_cont_ed_fields()
        self._parse_metadata()
        self._parse_fellowship_data()
        self._parse_custom_fields()
        return self._response

    def _parse_student_fields(self):
        self._response.student.username = StringParser(self._raw_data['Username']).parse()
        self._response.student.jhed = JHEDParser(self._raw_data['Auth Identifier']).parse()
        self._response.student.full_name = StringParser(self._raw_data['Name']).parse()

    def _parse_employment_fields(self):
        self._response.employment.employer_name = StringParser(self._raw_data['Employer Name']).parse()
        self._response.employment.employer_industry = StringParser(self._raw_data['Employer Industry']).parse()
        self._response.employment.employment_category = StringParser(self._raw_data['Employment Category']).parse()
        self._response.employment.employment_type = StringParser(self._raw_data['Employment Type']).parse()
        self._response.employment.job_function = StringParser(self._raw_data['Job Function']).parse()
        self._response.employment.job_title = StringParser(self._raw_data['Job Position']).parse()
        self._response.employment.found_through_handshake = YesNoParser(self._raw_data['Found through Handshake']).parse()
        self._response.employment.employed_during_education = YesNoParser(self._raw_data['Employed During Education']).parse()
        self._response.employment.salary = IntParser(self._raw_data['Salary']).parse()
        self._response.employment.bonus_amount = IntParser(self._raw_data['Bonus Amount']).parse()
        self._response.employment.other_compensation = IntParser(self._raw_data['Other Compensation']).parse()
        self._response.employment.is_internship = YesNoParser(self._raw_data['Internship']).parse()
        self._response.employment.offer_date = DateParser(self._raw_data['Offer Date']).parse()
        self._response.employment.accept_date = DateParser(self._raw_data['Accept Date']).parse()
        self._response.employment.start_date = DateParser(self._raw_data['Start Date']).parse()

    def _parse_cont_ed_fields(self):
        self._response.cont_ed.school = StringParser(self._raw_data['Continuing Education School']).parse()
        self._response.cont_ed.level = StringParser(self._raw_data['Continuing Education Level']).parse()
        self._response.cont_ed.major = StringParser(self._raw_data['Continuing Education Major']).parse()

    def _parse_metadata(self):
        self._response.metadata.response_id = StringParser(self._raw_data['Id']).parse()
        self._response.metadata.response_datetime_utc = DatetimeParser(self._raw_data['Response Date']).parse()
        self._parse_outcome()
        self._response.metadata.location = StringParser(self._raw_data['Location']).parse()
        self._response.metadata.submitted_by = StringParser(self._raw_data['Submitted By']).parse()
        self._response.metadata.is_knowledge_response = YesNoParser(self._raw_data['Knowledge Response?']).parse()
        self._response.metadata.knowledge_source = StringParser(self._raw_data['Knowledge Source']).parse()

    def _parse_outcome(self):
        if self._response_is_fellowship():
            self._response.metadata.outcome = 'Fellowship'
        else:
            self._response.metadata.outcome = StringParser(self._raw_data['Outcome']).parse()

    def _parse_fellowship_data(self):
        self._parse_fellowship_org()
        self._response.fellowship_data.fellowship_name = StringParser(self._raw_data['Fellowship Name']).parse()

    def _parse_fellowship_org(self):
        if self._response_is_fellowship():
            if self._raw_data['Outcome'] == 'Working':
                self._response.fellowship_data.fellowship_org = StringParser(self._raw_data['Employer Name']).parse()
            elif self._raw_data['Outcome'] == 'Continuing Education':
                self._response.fellowship_data.fellowship_org = StringParser(self._raw_data['Continuing Education School']).parse()

    def _response_is_fellowship(self):
        return self._raw_data['Is Fellowship?'] == 'Yes'

    def _parse_custom_fields(self):
        self._response = self._custom_parser.parse(self._response, self._raw_data)
