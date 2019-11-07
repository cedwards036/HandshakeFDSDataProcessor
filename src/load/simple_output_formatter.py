from typing import List

from src.load.response_formatter import ResponseFormatter
from src.survey_data_model import JHUDegree
from src.survey_data_model import SurveyResponse


class SimpleOutputFormatter(ResponseFormatter):

    def format(self, response: SurveyResponse) -> List[dict]:
        self._result = response.to_dict()
        self._flatten_location_fields()
        self._flatten_jhu_degrees()
        self._custom_formatter.format(self._result)
        return [self._column_order.apply_to(self._result)]

    def _flatten_location_fields(self):
        self._result.update(self._result['location'])
        del self._result['location']

    def _flatten_jhu_degrees(self):
        self._result.update(_DegreeFormatter(self._result['jhu_degrees']).format())
        del self._result['jhu_degrees']


class _DegreeFormatter:

    def __init__(self, degrees: List[JHUDegree]):
        self._degrees = degrees

    def format(self) -> dict:
        self._result = {'jhu_majors': set(), 'jhu_colleges': set()}
        self._parse_degree_data_into_result_dict()
        self._format_result()
        return self._result

    def _parse_degree_data_into_result_dict(self):
        for degree_record in self._degrees:
            self._result['jhu_majors'].add(f'{degree_record.degree}: {degree_record.major}')
            self._result['jhu_colleges'].add(degree_record.college)

    def _format_result(self):
        for field in self._result:
            self._result[field] = self._format_field(field)

    def _format_field(self, field):
        if not self._result[field]:
            return None
        else:
            return '; '.join(sorted(self._result[field]))
