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

    class UnexpectedValueException(Exception):
        pass


class StringParser(ValueParser):

    def parser_func(self):
        return self._value


class DatetimeParser(ValueParser):

    def parser_func(self):
        return datetime.strptime(self._value[:-4], '%Y-%m-%d %H:%M:%S')


class DateParser(ValueParser):

    def parser_func(self):
        return datetime.strptime(self._value, '%m/%d/%Y')


class IntParser(ValueParser):

    def parser_func(self):
        try:
            return int(self._value)
        except ValueError:
            raise self.UnexpectedValueException(f'Expected value "{self._value}" to be convertible to an int')


class YesNoParser(ValueParser):

    def parser_func(self):
        if self._value == 'Yes':
            return True
        elif self._value == 'No':
            return False
        else:
            raise self.UnexpectedValueException(f'Value was expected to be "Yes", "No", or "", but was "{self._value}" instead')
