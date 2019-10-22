from copy import deepcopy
from datetime import datetime

from src.survey_response.continuing_education_data import ContinuingEducationData
from src.survey_response.custom_questions import CustomQuestions, NullCustomQuestions
from src.survey_response.employment_data import EmploymentData
from src.survey_response.student_data import StudentData


class SurveyResponse:

    def __init__(self, custom_questions: CustomQuestions = NullCustomQuestions()):
        self.student = StudentData()
        self.employment = EmploymentData()
        self.cont_ed = ContinuingEducationData()
        self.custom = custom_questions
        self._data = {
            'response_id': None,
            'username': None,
            'response_datetime_utc': None,
            'outcome': None,
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


    def to_dict(self) -> dict:
        result = deepcopy(self._data)
        return result

    def __eq__(self, other: 'SurveyResponse') -> bool:
        return self.to_dict() == other.to_dict()
