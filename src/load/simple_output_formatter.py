from src.load.response_formatter import ResponseFormatter
from src.survey_data_model import SurveyResponse


class SimpleOutputFormatter(ResponseFormatter):

    def format(self, response: SurveyResponse) -> dict:
        result = response.to_dict()
        result = self._flatten_location_fields(result)
        result = self._custom_formatter.format(result)
        return result

    def _flatten_location_fields(self, response_dict: dict):
        response_dict.update(response_dict['location'])
        del response_dict['location']
        return response_dict
