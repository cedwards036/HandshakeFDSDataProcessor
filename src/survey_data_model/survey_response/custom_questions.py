from abc import ABC, abstractmethod
from typing import Union


class IntResponse:

    def __init__(self, value: Union[int, None]):
        self._value = value

    @property
    def value(self) -> Union[int, None]:
        return self._value

    @value.setter
    def value(self, new_value: Union[int, None]):
        self._value = new_value

    def __add__(self, other):
        return self._add(other)

    def __radd__(self, other):
        return self._add(other)

    def _add(self, other):
        if self._value == None:
            return self._add_none_to_other(other)
        else:
            return self._value + other

    def _add_none_to_other(self, other):
        if isinstance(other, IntResponse):
            return other.value
        else:
            return other


class ActivityQuestionSet:

    def __init__(self):
        self.name = None
        self._unpaid_count = IntResponse(None)
        self._paid_count = IntResponse(None)
        self._all_count = None

    @property
    def unpaid_count(self) -> int:
        return self._unpaid_count.value

    @unpaid_count.setter
    def unpaid_count(self, count: int):
        self._unpaid_count.value = count
        self._update_all_count()

    @property
    def paid_count(self) -> int:
        return self._paid_count.value

    @paid_count.setter
    def paid_count(self, count: int):
        self._paid_count.value = count
        self._update_all_count()

    def _update_all_count(self):
        self._all_count = self._unpaid_count + self._paid_count

    @property
    def all_count(self) -> int:
        return self._all_count

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'unpaid_count': self._unpaid_count.value,
            'paid_count': self._paid_count.value,
            'all_count': self._all_count,
        }


class CustomQuestions(ABC):

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class NullCustomQuestions(CustomQuestions):

    def to_dict(self) -> dict:
        return {}


class FDS2018CustomQuestions(CustomQuestions):

    def __init__(self):
        self.is_gap_year = None
        self._internships = self._initialize_internship_question_set()
        self._research = self._initialize_research_question_set()
        self._unpaid_internships_count = IntResponse(None)
        self._paid_internships_count = IntResponse(None)
        self._all_internships_count = None
        self._unpaid_research_count = IntResponse(None)
        self._paid_research_count = IntResponse(None)
        self._all_research_count = None

    def _initialize_internship_question_set(self) -> ActivityQuestionSet:
        internships = ActivityQuestionSet()
        internships.name = 'internships'
        return internships

    def _initialize_research_question_set(self) -> ActivityQuestionSet:
        research = ActivityQuestionSet()
        research.name = 'research'
        return research

    @property
    def unpaid_internships_count(self) -> int:
        return self._internships.unpaid_count

    @unpaid_internships_count.setter
    def unpaid_internships_count(self, count: int):
        self._internships.unpaid_count = count

    @property
    def paid_internships_count(self) -> int:
        return self._internships.paid_count

    @paid_internships_count.setter
    def paid_internships_count(self, count: int):
        self._internships.paid_count = count

    @property
    def all_internships_count(self) -> Union[int, None]:
        return self._internships.all_count

    @property
    def unpaid_research_count(self) -> int:
        return self._research.unpaid_count

    @unpaid_research_count.setter
    def unpaid_research_count(self, count: int):
        self._research.unpaid_count = count

    @property
    def paid_research_count(self) -> int:
        return self._research.paid_count

    @paid_research_count.setter
    def paid_research_count(self, count: int):
        self._research.paid_count = count

    @property
    def all_research_count(self) -> Union[int, None]:
        return self._research._all_count

    def to_dict(self) -> dict:
        return {
            'is_gap_year': self.is_gap_year,
            'internships': self._internships.to_dict(),
            'research': self._research.to_dict()
        }

    def __eq__(self, other: 'FDS2018CustomQuestions') -> bool:
        return self.to_dict() == other.to_dict()


class FDS2019ActivityQuestionSet(ActivityQuestionSet):

    def __init__(self):
        super().__init__()
        self.gained_valuable_skills = None
        self.connected_with_mentor = None
        self.may_lead_to_future_opps = None
        self.gained_clarity = None

    def to_dict(self) -> dict:
        result = super().to_dict()
        result['gained_valuable_skills'] = self.gained_valuable_skills
        result['connected_with_mentor'] = self.connected_with_mentor
        result['may_lead_to_future_opps'] = self.may_lead_to_future_opps
        result['gained_clarity'] = self.gained_clarity
        return result


class FDS2019CustomQuestions(CustomQuestions):

    def __init__(self):
        self.is_gap_year = None
        self.internships = self._initialize_internship_question_set()
        self.research = self._initialize_research_question_set()
        self._initialize_internship_question_set()
        self._initialize_research_question_set()

    def _initialize_internship_question_set(self) -> ActivityQuestionSet:
        internships = FDS2019ActivityQuestionSet()
        internships.name = 'internships'
        return internships

    def _initialize_research_question_set(self) -> ActivityQuestionSet:
        research = FDS2019ActivityQuestionSet()
        research.name = 'research'
        return research

    def to_dict(self) -> dict:
        return {
            'is_gap_year': self.is_gap_year,
            'internships': self.internships.to_dict(),
            'research': self.research.to_dict()
        }
