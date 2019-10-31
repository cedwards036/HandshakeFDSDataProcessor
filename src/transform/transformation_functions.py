from src.survey_data_model import ResponseDataset
from src.transform.csv_utils import csv_to_list_of_dicts
from src.transform.location_map import build_location_map


def transform_2019_fds_data(dataset: ResponseDataset, location_map_filepath: str) -> ResponseDataset:
    location_map = _get_location_map(location_map_filepath)
    for response in dataset:
        response.metadata.location = location_map.get_mapping(response.metadata.location)
    return dataset


def _get_location_map(filepath: str):
    raw_data = csv_to_list_of_dicts(filepath)
    return build_location_map(raw_data)
