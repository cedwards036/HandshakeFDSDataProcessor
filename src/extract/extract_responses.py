from typing import List

from src.extract.file_utils import read_csv
from src.extract.value_parser import DateParser, DatetimeParser
from src.survey_response import SurveyResponse


def extract_raw_responses(filepath: str) -> List[dict]:
    return read_csv(filepath)


class ResponseParser:

    def __init__(self, raw_data: dict):
        self._raw_data = raw_data
        self._response = SurveyResponse()

    def parse(self) -> SurveyResponse:
        self._response.response_datetime_utc = DatetimeParser(self._raw_data['Response Date']).parse()
        self._parse_employment_fields()
        return self._response

    def _parse_employment_fields(self):
        self._response.employment_data.offer_date = DateParser(self._raw_data['Offer Date']).parse()
        self._response.employment_data.accept_date = DateParser(self._raw_data['Accept Date']).parse()
        self._response.employment_data.start_date = DateParser(self._raw_data['Start Date']).parse()
