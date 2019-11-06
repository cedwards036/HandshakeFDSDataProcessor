import re
from abc import ABC, abstractmethod
from datetime import datetime

from src.survey_data_model import Location


class ValueParser(ABC):

    def __init__(self, value: str):
        self._value = value.strip()

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
        try:
            return datetime.strptime(self._value, '%m/%d/%Y')
        except ValueError:
            return datetime.strptime(self._value, '%Y-%m-%d')


class IntParser(ValueParser):

    def parser_func(self):
        try:
            return int(self._value)
        except ValueError:
            raise self.UnexpectedValueException(f'Expected value "{self._value}" to be convertible to an int')


class FloatParser(ValueParser):

    def parser_func(self):
        try:
            return float(self._value)
        except ValueError:
            raise self.UnexpectedValueException(f'Expected value "{self._value}" to be convertible to a float')


class YesNoParser(ValueParser):

    def parser_func(self):
        if self._value == 'Yes':
            return True
        elif self._value == 'No':
            return False
        else:
            raise self.UnexpectedValueException(f'Value was expected to be "Yes", "No", or "", but was "{self._value}" instead')


class JHEDParser(ValueParser):

    def parser_func(self):
        try:
            return self._extract_jhed_from_valid_value()
        except AttributeError:
            raise self.UnexpectedValueException(f'Cannot extract JHED from input value "{self._value}"')

    def _extract_jhed_from_valid_value(self) -> str:
        return re.match(r'^([a-zA-Z]+\d+)(@johnshopkins\.edu)?$', self._value).groups()[0]


class LocationParser(ValueParser):

    def parse(self):
        if self._value == '':
            return Location()
        else:
            return self.parser_func()

    def parser_func(self):
        values = [value.strip() for value in self._value.split(',')]
        if len(values) == 1:
            return Location(city=values[0])
        elif len(values) == 2:
            return Location(city=values[0], state=values[1])
        elif len(values) == 3:
            return Location(city=values[0], state=values[1], country=values[2])
        else:
            country = ', '.join(values[2:])
            return Location(city=values[0], state=values[1], country=country)
