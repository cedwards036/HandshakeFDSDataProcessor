from typing import Union, List

from src.extract.custom_parsers import CustomParser, NullCustomParser
from src.extract.value_parser import (StringParser, DateParser, DatetimeParser,
                                      YesNoParser, JHEDParser, FloatParser,
                                      LocationParser)
from src.survey_data_model import ResponseDataset
from src.survey_data_model import SurveyResponse


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
        self._parse_other_outcomes_data()
        self._parse_custom_fields()
        return self._response

    def _parse_student_fields(self):
        self._response.student.username = StringParser(self._raw_data['Username']).parse()
        self._response.student.email = StringParser(self._raw_data['School Email']).parse()
        self._response.student.jhed = JHEDParser(self._raw_data['Auth Identifier']).parse()
        self._response.student.full_name = StringParser(self._raw_data['Name']).parse()

    def _parse_employment_fields(self):
        self._response.employment.employer_name = self._parse_employer_name()
        self._response.employment.employer_industry = StringParser(self._raw_data['Employer Industry']).parse()
        self._response.employment.employment_category = StringParser(self._raw_data['Employment Category']).parse()
        self._response.employment.employment_type = self._parse_employment_type()
        self._response.employment.job_function = StringParser(self._raw_data['Job Function']).parse()
        self._response.employment.job_title = self._parse_job_title()
        self._response.employment.found_through_handshake = YesNoParser(self._raw_data['Found through Handshake']).parse()
        self._response.employment.employed_during_education = YesNoParser(self._raw_data['Employed During Education']).parse()
        self._response.employment.salary = FloatParser(self._raw_data['Annual Salary']).parse()
        self._response.employment.bonus_amount = FloatParser(self._raw_data['Bonus Amount']).parse()
        self._response.employment.other_compensation = FloatParser(self._raw_data['Other Compensation']).parse()
        self._response.employment.is_internship = YesNoParser(self._raw_data['Internship']).parse()
        self._response.employment.offer_date = DateParser(self._raw_data['Offer Date']).parse()
        self._response.employment.accept_date = DateParser(self._raw_data['Accept Date']).parse()
        self._response.employment.start_date = DateParser(self._raw_data['Start Date']).parse()

    def _parse_employer_name(self) -> Union[str, None]:
        if self._is_military_response():
            return StringParser(self._raw_data['Military Branch']).parse()
        else:
            return StringParser(self._raw_data['Employer Name']).parse()

    def _is_military_response(self) -> bool:
        return self._raw_data['Outcome'] == 'Military'

    def _parse_employment_type(self):
        if self._is_military_response():
            return 'Full-Time'
        else:
            return StringParser(self._raw_data['Employment Type']).parse()

    def _parse_job_title(self) -> Union[str, None]:
        if self._is_military_response():
            return self._parse_military_job_title()
        else:
            return StringParser(self._raw_data['Job Position']).parse()

    def _parse_military_job_title(self) -> Union[str, None]:
        rank = self._raw_data['Military Rank']
        specialization = self._raw_data['Specialization']
        if not rank and not specialization:
            return None
        elif not rank:
            return StringParser(f'{specialization} Specialist').parse()
        elif not specialization:
            return StringParser(rank).parse()
        else:
            return StringParser(f'{specialization} {rank}').parse()

    def _parse_cont_ed_fields(self):
        self._response.cont_ed.school = StringParser(self._raw_data['Continuing Education School']).parse()
        self._response.cont_ed.level = StringParser(self._raw_data['Continuing Education Level']).parse()
        self._response.cont_ed.major = StringParser(self._raw_data['Continuing Education Major']).parse()

    def _parse_metadata(self):
        self._response.metadata.response_id = StringParser(self._raw_data['Id']).parse()
        self._response.metadata.survey_id = StringParser(self._raw_data['Survey ID']).parse()
        self._response.metadata.response_datetime_utc = DatetimeParser(self._raw_data['Response Date']).parse()
        self._response.metadata.outcome = self._parse_outcome()
        self._response.metadata.location = LocationParser(self._raw_data['Location']).parse()
        self._response.metadata.submitted_by = StringParser(self._raw_data['Submitted By']).parse()
        self._response.metadata.is_knowledge_response = YesNoParser(self._raw_data['Knowledge Response?']).parse()
        self._response.metadata.knowledge_source = StringParser(self._raw_data['Knowledge Source']).parse()
        self._response.metadata.is_submitted = StringParser(self._raw_data['Response Status']).parse() == 'submitted'

    def _parse_outcome(self) -> Union[str, None]:
        if self._response_is_fellowship():
            return 'Fellowship'
        else:
            return StringParser(self._raw_data['Outcome']).parse()

    def _parse_fellowship_data(self):
        self._response.fellowship_data.fellowship_org = self._parse_fellowship_org()
        self._response.fellowship_data.fellowship_name = StringParser(self._raw_data['Fellowship Name']).parse()

    def _parse_fellowship_org(self) -> Union[str, None]:
        if self._response_is_fellowship():
            if self._raw_data['Outcome'] == 'Working':
                return StringParser(self._raw_data['Employer Name']).parse()
            elif self._raw_data['Outcome'] == 'Continuing Education':
                return StringParser(self._raw_data['Continuing Education School']).parse()

    def _response_is_fellowship(self):
        return self._raw_data['Is Fellowship?'] == 'Yes'

    def _parse_custom_fields(self):
        self._response = self._custom_parser.parse(self._response, self._raw_data)

    def _parse_other_outcomes_data(self):
        self._response.other_outcomes.still_looking_option = StringParser(self._raw_data['Still Looking Option']).parse()
        self._response.other_outcomes.not_seeking_option = StringParser(self._raw_data['Not Seeking Option']).parse()


def parse_responses(raw_data: List[dict], custom_parser: CustomParser) -> ResponseDataset:
    result = ResponseDataset()
    for row in raw_data:
        result.add_response(ResponseParser(row, custom_parser).parse())
    return result
