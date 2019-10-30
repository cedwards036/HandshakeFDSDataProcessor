from src.survey_data_model.survey_response.continuing_education_data import ContinuingEducationData
from src.survey_data_model.survey_response.custom_questions import CustomQuestions, NullCustomQuestions
from src.survey_data_model.survey_response.employment_data import EmploymentData
from src.survey_data_model.survey_response.fellowship_data import FellowshipData
from src.survey_data_model.survey_response.metadata import Metadata
from src.survey_data_model.survey_response.other_outcomes_data import OtherOutcomesData
from src.survey_data_model.survey_response.student_data import StudentData


class SurveyResponse:

    def __init__(self, custom_questions: CustomQuestions = NullCustomQuestions()):
        self.student = StudentData()
        self.employment = EmploymentData()
        self.cont_ed = ContinuingEducationData()
        self.metadata = Metadata()
        self.fellowship_data = FellowshipData()
        self.other_outcomes = OtherOutcomesData()
        self.custom = custom_questions

    def to_dict(self) -> dict:
        result = {}
        result.update(self.student.to_dict())
        result.update(self.employment.to_dict())
        result.update(self.cont_ed.to_dict())
        result.update(self.metadata.to_dict())
        result.update(self.fellowship_data.to_dict())
        result.update(self.other_outcomes.to_dict())
        result.update(self.custom.to_dict())
        return result

    def __eq__(self, other: 'SurveyResponse') -> bool:
        return self.to_dict() == other.to_dict()
