from abc import ABC, abstractmethod

from src.load.custom_formatters import CustomFormatter, NullCustomFormatter
from src.survey_data_model import SurveyResponse


class ResponseFormatter(ABC):

    def __init__(self, custom_formatter: CustomFormatter = NullCustomFormatter()):
        self._custom_formatter = custom_formatter

    @abstractmethod
    def format(self, response: SurveyResponse) -> dict:
        pass
