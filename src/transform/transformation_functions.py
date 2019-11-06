from src.survey_data_model import ResponseDataset, SurveyResponse
from src.transform.csv_utils import csv_to_list_of_dicts
from src.transform.is_jhu import is_jhu
from src.transform.value_map import ValueMapBuilder


def transform_2019_fds_data(dataset: ResponseDataset, mapping_filepaths: dict) -> ResponseDataset:
    mappings = Mappings(mapping_filepaths)
    for response in dataset:
        ResponseCleaner(mappings, response).clean()
    return dataset


class Mappings:

    def __init__(self, mapping_filepaths: dict):
        self._mapping_filepaths = mapping_filepaths
        self._load_location_map()
        self._load_employer_name_map()
        self._load_cont_ed_maps()
        self._load_jhu_degree_map()

    def _load_location_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['location'])
        self.location_map = ValueMapBuilder.build_location_map(raw_data)

    def _load_employer_name_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['employer_name'])
        self.employer_name_map = ValueMapBuilder.build_cached_value_map(raw_data, 'old_value', 'new_value')

    def _load_cont_ed_maps(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['cont_ed'])
        self.college_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'clean_college')
        self.major_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'clean_major')
        self.degree_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'degree')
        self.major_group_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'major_group')

    def _load_jhu_degree_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['jhu_degree'])
        self.jhu_degree_map = ValueMapBuilder.build_jhu_degree_map(raw_data)


class ResponseCleaner:

    def __init__(self, mappings: Mappings, response: SurveyResponse):
        self._response = response
        self._mappings = mappings

    def clean(self):
        self._clean_locations()
        self._set_is_jhu()
        self._clean_employer_names()
        self._clean_cont_ed_data()
        self._add_jhu_degree_info()

    def _clean_locations(self):
        self._response.metadata.location = self._mappings.location_map.get_mapping(self._response.metadata.location)

    def _set_is_jhu(self):
        self._response.metadata.is_jhu = is_jhu(self._response.cont_ed.school) or is_jhu(self._response.employment.employer_name)

    def _clean_employer_names(self):
        self._response.employment.employer_name = self._mappings.employer_name_map.get_mapping(self._response.employment.employer_name)

    def _clean_cont_ed_data(self):
        if self._response.metadata.outcome == 'Continuing Education':
            self._response.cont_ed.school = self._mappings.college_map.get_mapping(self._response.student.email)
            self._response.cont_ed.major = self._mappings.major_map.get_mapping(self._response.student.email)
            self._response.cont_ed.degree = self._mappings.degree_map.get_mapping(self._response.student.email)
            self._response.cont_ed.major_group = self._mappings.major_group_map.get_mapping(self._response.student.email)

    def _add_jhu_degree_info(self):
        self._response.student.jhu_degrees = self._mappings.jhu_degree_map.get_mapping(self._response.student.email)
