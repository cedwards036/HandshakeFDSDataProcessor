from abc import ABC, abstractmethod
from datetime import datetime


class ValueParser(ABC):

    def __init__(self, value: str):
        self._value = value

    def parse(self):
        if self._value == '':
            return None
        else:
            return self.parser_func()

    @abstractmethod
    def parser_func(self):
        pass


class DatetimeParser(ValueParser):

    def parser_func(self):
        return datetime.strptime(self._value[:-4], '%Y-%m-%d %H:%M:%S')


class DateParser(ValueParser):

    def parser_func(self):
        return datetime.strptime(self._value, '%m/%d/%Y')
