from typing import List

from src.load.response_formatter import ResponseFormatter
from src.survey_data_model import ResponseDataset


def format_dataset(dataset: ResponseDataset, formatter: ResponseFormatter) -> List[dict]:
    return [formatter.format(response) for response in dataset]
