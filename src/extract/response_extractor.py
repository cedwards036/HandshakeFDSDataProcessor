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
        self._field_lookup[value] += 1
        if self._value_is_duplicate_field(value):
            return self._format_duplicate_field_name(value)
        else:
            return value

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
        for i, value in enumerate(row):
            result_row[self._fields[i]] = value
        return result_row
