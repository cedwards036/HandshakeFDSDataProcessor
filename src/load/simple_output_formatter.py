from src.survey_data_model import SurveyResponse


class SimpleOutputFormatter:

    def __init__(self, response: SurveyResponse):
        self._response = response

    def format(self) -> dict:
        result = self._response.to_dict()
        result = self._flatten_location_fields(result)
        return result

    def _flatten_location_fields(self, response_dict: dict):
        response_dict.update(response_dict['location'])
        del response_dict['location']
        return response_dict
