from datetime import datetime
from typing import Union


class EmploymentData:

    def __init__(self):
        self._data = {
            'offer_date': None,
            'accept_date': None,
            'start_date': None,
        }

    @property
    def offer_date(self) -> Union[datetime, None]:
        return self._data['offer_date']

    @offer_date.setter
    def offer_date(self, new_date: datetime):
        self._data['offer_date'] = new_date

    @property
    def accept_date(self) -> Union[datetime, None]:
        return self._data['accept_date']

    @accept_date.setter
    def accept_date(self, new_date: datetime):
        self._data['accept_date'] = new_date

    @property
    def start_date(self) -> Union[datetime, None]:
        return self._data['start_date']

    @start_date.setter
    def start_date(self, new_date: datetime):
        self._data['start_date'] = new_date

    def to_dict(self) -> dict:
        result = self._data.copy()
        return result

    def __eq__(self, other: 'EmploymentData') -> bool:
        return self.to_dict() == other.to_dict()
