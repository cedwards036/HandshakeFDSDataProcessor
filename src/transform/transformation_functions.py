from src.survey_data_model import ResponseDataset, SurveyResponse
from src.transform.build_value_map import build_value_map
from src.transform.csv_utils import csv_to_list_of_dicts
from src.transform.is_jhu import is_jhu
from src.transform.location_map import build_location_map


def transform_2019_fds_data(dataset: ResponseDataset, mapping_filepaths: dict) -> ResponseDataset:
    mappings = Mappings(mapping_filepaths)
    for response in dataset:
        ResponseCleaner(mappings, response).clean()
    return dataset


class Mappings:

    def __init__(self, mapping_filepaths: dict):
        self._mapping_filepaths = mapping_filepaths
        self.location_map = self._get_location_map()
        self.employer_name_map = self._get_employer_name_map()

    def _get_location_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['location'])
        return build_location_map(raw_data)

    def _get_employer_name_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['employer_name'])
        return build_value_map(raw_data, 'old_value', 'new_value')


class ResponseCleaner:

    def __init__(self, mappings: Mappings, response: SurveyResponse):
        self._response = response
        self._mappings = mappings

    def clean(self):
        self._clean_locations()
        self._set_is_jhu()
        self._clean_employer_names()

    def _clean_locations(self):
        self._response.metadata.location = self._mappings.location_map.get_mapping(self._response.metadata.location)

    def _set_is_jhu(self):
        self._response.metadata.is_jhu = is_jhu(self._response.cont_ed.school) or is_jhu(self._response.employment.employer_name)

    def _clean_employer_names(self):
        self._response.employment.employer_name = self._mappings.employer_name_map.get_mapping(self._response.employment.employer_name)
