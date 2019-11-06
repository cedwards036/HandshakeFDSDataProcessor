from abc import ABC, abstractmethod

from src.load.column_order import ColumnOrder, NullColumnOrder
from src.load.custom_formatters import CustomFormatter, NullCustomFormatter
from src.survey_data_model import SurveyResponse


class ResponseFormatter(ABC):

    def __init__(self, custom_formatter: CustomFormatter = NullCustomFormatter(),
                 column_order: ColumnOrder = NullColumnOrder()):
        self._custom_formatter = custom_formatter
        self._column_order = column_order

    @abstractmethod
    def format(self, response: SurveyResponse) -> dict:
        pass
