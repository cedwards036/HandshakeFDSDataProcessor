from copy import deepcopy

from src.survey_response.continuing_education_data import ContinuingEducationData
from src.survey_response.custom_questions import CustomQuestions, NullCustomQuestions
from src.survey_response.employment_data import EmploymentData
from src.survey_response.metadata import Metadata
from src.survey_response.student_data import StudentData


class SurveyResponse:

    def __init__(self, custom_questions: CustomQuestions = NullCustomQuestions()):
        self.student = StudentData()
        self.employment = EmploymentData()
        self.cont_ed = ContinuingEducationData()
        self.metadata = Metadata()
        self.custom = custom_questions
        self._data = {
            'fellowship_org': None,
            'fellowship_name': None,
            'still_seeking_option': None,
            'not_seeking_option': None,
        }

    def to_dict(self) -> dict:
        result = deepcopy(self._data)
        return result

    def __eq__(self, other: 'SurveyResponse') -> bool:
        return self.to_dict() == other.to_dict()
