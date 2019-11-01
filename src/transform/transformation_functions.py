from src.survey_data_model import ResponseDataset, SurveyResponse
from src.transform.build_value_map import build_value_map
from src.transform.csv_utils import csv_to_list_of_dicts
from src.transform.is_jhu import is_jhu
from src.transform.location_map import build_location_map


def transform_2019_fds_data(dataset: ResponseDataset, mapping_filepaths: dict) -> ResponseDataset:
    location_map = _get_location_map(mapping_filepaths['location'])
    employer_name_map = _get_employer_name_map(mapping_filepaths['employer_name'])
    response: SurveyResponse
    for response in dataset:
        response.metadata.location = location_map.get_mapping(response.metadata.location)
        response.employment.employer_name = employer_name_map.get_mapping(response.employment.employer_name)
        _set_is_jhu(response)
    return dataset


def _set_is_jhu(response):
    response.metadata.is_jhu = is_jhu(response.cont_ed.school) or is_jhu(response.employment.employer_name)


def _get_location_map(filepath: str):
    raw_data = csv_to_list_of_dicts(filepath)
    return build_location_map(raw_data)


def _get_employer_name_map(filepath: str):
    raw_data = csv_to_list_of_dicts(filepath)
    return build_value_map(raw_data, 'old_value', 'new_value')
