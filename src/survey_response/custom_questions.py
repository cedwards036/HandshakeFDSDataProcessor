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


class CustomQuestions:

    def __init__(self):
        self._data = {
            'is_gap_year': None,
            'unpaid_internships_count': IntResponse(None),
            'paid_internships_count': IntResponse(None),
            'all_internships_count': None,
            'unpaid_research_count': IntResponse(None),
            'paid_research_count': IntResponse(None),
            'all_research_count': None
        }

    @property
    def unpaid_internships_count(self) -> int:
        return self._data['unpaid_internships_count'].value

    @unpaid_internships_count.setter
    def unpaid_internships_count(self, count: int):
        self._data['unpaid_internships_count'] = count
        self._update_all_internships_count()

    @property
    def paid_internships_count(self) -> int:
        return self._data['paid_internships_count'].value

    @paid_internships_count.setter
    def paid_internships_count(self, count: int):
        self._data['paid_internships_count'] = count
        self._update_all_internships_count()

    def _update_all_internships_count(self):
        self._data['all_internships_count'] = self._data['unpaid_internships_count'] + self._data['paid_internships_count']

    @property
    def all_internships_count(self) -> Union[int, None]:
        return self._data['all_internships_count']

    @property
    def unpaid_research_count(self) -> int:
        return self._data['unpaid_research_count'].value

    @unpaid_research_count.setter
    def unpaid_research_count(self, count: int):
        self._data['unpaid_research_count'] = count
        self._update_all_research_count()

    @property
    def paid_research_count(self) -> int:
        return self._data['paid_research_count'].value

    @paid_research_count.setter
    def paid_research_count(self, count: int):
        self._data['paid_research_count'] = count
        self._update_all_research_count()

    def _update_all_research_count(self):
        self._data['all_research_count'] = self._data['unpaid_research_count'] + self._data['paid_research_count']

    @property
    def all_research_count(self) -> Union[int, None]:
        return self._data['all_research_count']

    def to_dict(self) -> dict:
        result = self._data.copy()
        result['unpaid_internships_count'] = result['unpaid_internships_count'].value
        result['paid_internships_count'] = result['paid_internships_count'].value
        result['unpaid_research_count'] = result['unpaid_research_count'].value
        result['paid_research_count'] = result['paid_research_count'].value
        return result

    def __eq__(self, other: 'CustomQuestions') -> bool:
        return self.to_dict() == other.to_dict()
