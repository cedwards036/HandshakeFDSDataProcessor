from src.load.response_formatter import ResponseFormatter
from src.survey_data_model import SurveyResponse


class SimpleOutputFormatter(ResponseFormatter):

    def format(self, response: SurveyResponse) -> dict:
        self._result = response.to_dict()
        self._flatten_location_fields()
        self._flatten_jhu_degrees()
        self._custom_formatter.format(self._result)
        return self._result

    def _flatten_location_fields(self):
        self._result.update(self._result['location'])
        del self._result['location']

    def _flatten_jhu_degrees(self):
        if not self._result['jhu_degrees']:
            self._set_degree_fields_for_record_without_degree_data()
        else:
            self._set_degree_fields()

    def _set_degree_fields_for_record_without_degree_data(self):
        self._result['jhu_degrees'] = None
        self._result['jhu_majors'] = None
        self._result['jhu_colleges'] = None

    def _set_degree_fields(self):
        formatted_degree_info = self._build_formatted_degree_info_dict()
        self._result['jhu_degrees'] = formatted_degree_info['jhu_degrees']
        self._result['jhu_majors'] = formatted_degree_info['jhu_majors']
        self._result['jhu_colleges'] = formatted_degree_info['jhu_colleges']

    def _build_formatted_degree_info_dict(self) -> dict:
        formatted_degree_info = {'jhu_degrees': set(), 'jhu_majors': set(), 'jhu_colleges': set()}
        for degree_record in self._result['jhu_degrees']:
            formatted_degree_info['jhu_degrees'].add(degree_record.degree)
            formatted_degree_info['jhu_majors'].add(degree_record.major)
            formatted_degree_info['jhu_colleges'].add(degree_record.college)
        for field in formatted_degree_info:
            formatted_degree_info[field] = '; '.join(sorted(formatted_degree_info[field]))
        return formatted_degree_info
