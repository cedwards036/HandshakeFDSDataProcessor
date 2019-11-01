import csv
from collections import defaultdict
from typing import List


class _FieldNameParser:

    def __init__(self, row):
        self._row = row
        self._field_lookup = defaultdict(int)

    def parse(self) -> List[str]:
        result = []
        for i, value in enumerate(self._row):
            result.append(self._parse_field_name(value))
        return result

    def _parse_field_name(self, value) -> str:
        clean_value = self._remove_non_ascii_chars(value)
        self._field_lookup[clean_value] += 1
        if self._value_is_duplicate_field(clean_value):
            return self._format_duplicate_field_name(clean_value)
        else:
            return clean_value

    def _remove_non_ascii_chars(self, value: str) -> str:
        return value.replace('', '')

    def _value_is_duplicate_field(self, value):
        return self._field_lookup[value] > 1

    def _format_duplicate_field_name(self, value):
        return f'{value}_{self._field_lookup[value] - 1}'


class ResponseExtractor:

    def __init__(self, filepath: str):
        self._filepath = filepath

    def extract(self):
        with open(self._filepath, encoding='utf-8') as f:
            reader = csv.reader(f, skipinitialspace=True)
            self._fields = _FieldNameParser(next(reader)).parse()
            return self._build_result(reader)

    def _build_result(self, reader):
        result = []
        for row in reader:
            result.append(self._build_result_row(row))
        return result

    def _build_result_row(self, row):
        result_row = {}
        for i, field in enumerate(self._fields):
            result_row[field] = self._get_field_value(i, row)
        return result_row

    def _get_field_value(self, i: int, row: list):
        try:
            return row[i]
        except IndexError:
            return ''
