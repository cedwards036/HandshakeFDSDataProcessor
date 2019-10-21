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
            return other
        else:
            return self._value + other


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
        self._unpaid_internships_count = IntResponse(None)
        self._paid_internships_count = IntResponse(None)
        self._all_internships_count = None
        self._unpaid_research_count = IntResponse(None)
        self._paid_research_count = IntResponse(None)
        self._all_research_count = None

    @property
    def unpaid_internships_count(self) -> int:
        return self._unpaid_internships_count.value

    @unpaid_internships_count.setter
    def unpaid_internships_count(self, count: int):
        self._unpaid_internships_count.value = count
        self._update_all_internships_count()

    @property
    def paid_internships_count(self) -> int:
        return self._paid_internships_count.value

    @paid_internships_count.setter
    def paid_internships_count(self, count: int):
        self._paid_internships_count.value = count
        self._update_all_internships_count()

    def _update_all_internships_count(self):
        self._all_internships_count = self._unpaid_internships_count + self._paid_internships_count

    @property
    def all_internships_count(self) -> Union[int, None]:
        return self._all_internships_count

    @property
    def unpaid_research_count(self) -> int:
        return self._unpaid_research_count.value

    @unpaid_research_count.setter
    def unpaid_research_count(self, count: int):
        self._unpaid_research_count.value = count
        self._update_all_research_count()

    @property
    def paid_research_count(self) -> int:
        return self._paid_research_count.value

    @paid_research_count.setter
    def paid_research_count(self, count: int):
        self._paid_research_count.value = count
        self._update_all_research_count()

    def _update_all_research_count(self):
        self._all_research_count = self._unpaid_research_count + self._paid_research_count

    @property
    def all_research_count(self) -> Union[int, None]:
        return self._all_research_count

    def to_dict(self) -> dict:
        return {
            'is_gap_year': self.is_gap_year,
            'unpaid_internships_count': self._unpaid_internships_count.value,
            'paid_internships_count': self._paid_internships_count.value,
            'all_internships_count': self._all_internships_count,
            'unpaid_research_count': self._unpaid_research_count.value,
            'paid_research_count': self._paid_research_count.value,
            'all_research_count': self._all_research_count
        }

    def __eq__(self, other: 'FDS2018CustomQuestions') -> bool:
        return self.to_dict() == other.to_dict()
