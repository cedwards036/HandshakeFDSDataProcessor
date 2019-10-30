from abc import ABC, abstractmethod

from src.extract.value_parser import YesNoParser, IntParser, StringParser
from src.survey_response import SurveyResponse
from src.survey_response.custom_questions import (CustomQuestions,
                                                  FDS2018CustomQuestions,
                                                  FDS2019CustomQuestions,
                                                  NullCustomQuestions)


class CustomParser(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def parse(self, response: SurveyResponse, raw_data: dict) -> SurveyResponse:
        pass

    @abstractmethod
    def get_questions_class(self) -> CustomQuestions:
        pass


class FDS2018CustomParser(CustomParser):
    GAP_YEAR_QUESTION = 'At the time you accepted your current position, did you accept it with the intention that it would only be a temporary, “gap year” position, before applying to graduate or professional school in the next year or two?'
    UNPAID_INTERN_QUESTION = 'During your time at Hopkins, how many *unpaid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*. '
    PAID_INTERN_QUESTION = 'During your time at Hopkins, how many *paid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*.'
    UNPAID_RESEARCH_QUESTION = 'During your time at Hopkins, how many unique *unpaid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.'
    PAID_RESEARCH_QUESTION = 'During your time at Hopkins, how many unique *paid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.'

    def parse(self, response: SurveyResponse, raw_data: dict) -> SurveyResponse:
        response.custom.is_gap_year = YesNoParser(raw_data[self.GAP_YEAR_QUESTION]).parse()
        response.custom.unpaid_internships_count = IntParser(raw_data[self.UNPAID_INTERN_QUESTION]).parse()
        response.custom.paid_internships_count = IntParser(raw_data[self.PAID_INTERN_QUESTION]).parse()
        response.custom.unpaid_research_count = IntParser(raw_data[self.UNPAID_RESEARCH_QUESTION]).parse()
        response.custom.paid_research_count = IntParser(raw_data[self.PAID_RESEARCH_QUESTION]).parse()
        return response

    def get_questions_class(self) -> CustomQuestions:
        return FDS2018CustomQuestions()


class FDS2019CustomParser(CustomParser):
    GAP_YEAR_QUESTION = 'At the time you accepted your current position, did you accept it with the intention that it would only be a temporary, “gap year” position, before applying to graduate or professional school in the next year or two?'
    UNPAID_INTERN_QUESTION = 'During your time at Hopkins, how many *unpaid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*.'
    PAID_INTERN_QUESTION = 'During your time at Hopkins, how many *paid* internships did you participate in? An internship is a form of experiential education that integrates knowledge and theory learned in the classroom, with practical application and skill development *in a professional, work setting*.'
    UNPAID_RESEARCH_QUESTION = 'During your time at Hopkins, how many unique *unpaid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.'
    PAID_RESEARCH_QUESTION = 'During your time at Hopkins, how many unique *paid* research experiences (outside the classroom) did you participate in? Research is inquiry or investigation conducted by an undergraduate student that makes an original intellectual or creative contribution to a discipline. It can encompass a wide variety of activities including but not limited to: lab research, design projects, entrepreneurship, etc.'

    def parse(self, response: SurveyResponse, raw_data: dict) -> SurveyResponse:
        self._parse_gap_year_question(raw_data, response)
        self._parse_internships_questions(raw_data, response)
        self._parse_research_questions(raw_data, response)

        return response

    def _parse_gap_year_question(self, raw_data, response):
        response.custom.is_gap_year = YesNoParser(raw_data[self.GAP_YEAR_QUESTION]).parse()

    def _parse_internships_questions(self, raw_data, response):
        response.custom.internships.unpaid_count = IntParser(raw_data[self.UNPAID_INTERN_QUESTION]).parse()
        response.custom.internships.paid_count = IntParser(raw_data[self.PAID_INTERN_QUESTION]).parse()
        response.custom.internships.gained_valuable_skills = StringParser(raw_data['I gained valuable skills']).parse()
        response.custom.internships.connected_with_mentor = StringParser(raw_data['I connected with a mentor']).parse()
        response.custom.internships.may_lead_to_future_opps = StringParser(raw_data['This internship may lead to future opportunities']).parse()
        response.custom.internships.gained_clarity = StringParser(raw_data['I gained clarity about what I find meaningful']).parse()

    def _parse_research_questions(self, raw_data, response):
        response.custom.research.unpaid_count = IntParser(raw_data[self.UNPAID_RESEARCH_QUESTION]).parse()
        response.custom.research.paid_count = IntParser(raw_data[self.PAID_RESEARCH_QUESTION]).parse()
        response.custom.research.gained_valuable_skills = StringParser(raw_data['I gained valuable skills_1']).parse()
        response.custom.research.connected_with_mentor = StringParser(raw_data['I connected with a mentor_1']).parse()
        response.custom.research.may_lead_to_future_opps = StringParser(raw_data['This research experience may lead to future opportunities']).parse()
        response.custom.research.gained_clarity = StringParser(raw_data['I gained clarity about what I find meaningful_2']).parse()

    def get_questions_class(self) -> CustomQuestions:
        return FDS2019CustomQuestions()


class NullCustomParser(CustomParser):

    def parse(self, response: SurveyResponse, raw_data: dict) -> SurveyResponse:
        return response

    def get_questions_class(self) -> CustomQuestions:
        return NullCustomQuestions()
