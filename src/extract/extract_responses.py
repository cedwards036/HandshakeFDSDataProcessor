from typing import List

from src.extract.file_utils import read_csv
from src.extract.value_parser import DateParser, DatetimeParser
from src.survey_response import SurveyResponse


def extract_raw_responses(filepath: str) -> List[dict]:
    return read_csv(filepath)


def parse_response(raw_response: dict) -> SurveyResponse:
    response = SurveyResponse()
    response.response_datetime_utc = DatetimeParser(raw_response['Response Date']).parse()
    response.employment_data.offer_date = DateParser(raw_response['Offer Date']).parse()
    response.employment_data.accept_date = DateParser(raw_response['Accept Date']).parse()
    response.employment_data.start_date = DateParser(raw_response['Start Date']).parse()
    return response
