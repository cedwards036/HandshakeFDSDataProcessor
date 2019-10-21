from copy import deepcopy
from datetime import datetime
from typing import Union


class IntResponse:

    def __init__(self, value: Union[int, None]):
        self._value = value

    @property
    def value(self) -> Union[int, None]:
        return self._value

    def __add__(self, other):
        return self._add(other)

    def __radd__(self, other):
        return self._add(other)

    def _add(self, other):
        if self._value == None:
            return other
        else:
            return self._value + other


class SurveyResponse:

    def __init__(self):
        self._data = {
            'response_id': None,
            'username': None,
            'jhed': None,
            'full_name': None,
            'jhu_colleges': [],
            'jhu_majors': [],
            'gender': None,
            'visa_status': None,
            'response_datetime_utc': None,
            'outcome': None,
            'employer_name': None,
            'employer_industry': None,
            'employment_category': None,
            'employment_type': None,
            'job_function': None,
            'job_title': None,
            'found_through_handshake': None,
            'employed_during_education': None,
            'offer_date': None,
            'accept_date': None,
            'start_date': None,
            'salary': None,
            'bonus_amount': None,
            'other_compensation': None,
            'is_authorized_to_work_in_us': None,
            'is_internship': None,
            'cont_ed_school': None,
            'cont_ed_level': None,
            'cont_ed_degree': None,
            'cont_ed_major': None,
            'cont_ed_major_group': None,
            'fellowship_org': None,
            'fellowship_name': None,
            'still_seeking_option': None,
            'not_seeking_option': None,
            'location': None,
            'is_jhu': None,
            'submitted_by': None,
            'is_knowledge_response': None,
            'knowledge_source': None
        }

    @property
    def username(self) -> str:
        return self._data['username']

    @username.setter
    def username(self, new_username: str):
        self._data['username'] = new_username

    @property
    def response_datetime_utc(self) -> datetime:
        return self._data['response_datetime_utc']

    @response_datetime_utc.setter
    def response_datetime_utc(self, new_datetime: datetime):
        self._data['response_datetime_utc'] = new_datetime

    @property
    def offer_date(self) -> datetime:
        return self._data['offer_date']

    @offer_date.setter
    def offer_date(self, new_date: datetime):
        self._data['offer_date'] = new_date

    @property
    def accept_date(self) -> datetime:
        return self._data['accept_date']

    @accept_date.setter
    def accept_date(self, new_date: datetime):
        self._data['accept_date'] = new_date

    @property
    def start_date(self) -> datetime:
        return self._data['start_date']

    @start_date.setter
    def start_date(self, new_date: datetime):
        self._data['start_date'] = new_date

    def to_dict(self) -> dict:
        result = deepcopy(self._data)
        return result

    def __eq__(self, other: 'SurveyResponse') -> bool:
        return self.to_dict() == other.to_dict()
