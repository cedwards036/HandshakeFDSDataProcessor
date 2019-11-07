from typing import List

from src.load.response_formatter import ResponseFormatter
from src.survey_data_model import JHUDegree
from src.survey_data_model import SurveyResponse


class LongformFormatter(ResponseFormatter):

    def format(self, response: SurveyResponse) -> List[dict]:
        self._base_row = response.to_dict()
        self._flatten_location_fields()
        self._custom_formatter.format(self._base_row)
        return self._generate_one_row_per_degree()

    def _flatten_location_fields(self):
        self._base_row.update(self._base_row['location'])
        del self._base_row['location']

    def _generate_one_row_per_degree(self):
        if not self._base_row['jhu_degrees']:
            return self._format_row_without_degree()
        else:
            return self._format_row_with_degrees()

    def _format_row_without_degree(self):
        degree = JHUDegree(None, None, None)
        return [self._column_order.apply_to(self._make_row_copy(degree))]

    def _make_row_copy(self, degree):
        row_copy = self._base_row.copy()
        del row_copy['jhu_degrees']
        row_copy['jhu_degree'] = degree.degree
        row_copy['jhu_major'] = degree.major
        row_copy['jhu_college'] = degree.college
        return self._column_order.apply_to(row_copy)

    def _format_row_with_degrees(self):
        result = []
        for degree in self._base_row['jhu_degrees']:
            result.append(self._make_row_copy(degree))
        return result
