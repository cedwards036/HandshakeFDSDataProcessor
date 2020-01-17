from typing import Union

from src.survey_data_model import ResponseDataset, SurveyResponse
from src.transform.csv_utils import csv_to_list_of_dicts
from src.transform.is_jhu import is_jhu
from src.transform.value_map import ValueMapBuilder, ValueMap


def transform_2019_fds_data(dataset: ResponseDataset, mapping_filepaths: dict) -> ResponseDataset:
    mappings = Mappings(mapping_filepaths)
    for response in dataset:
        ResponseCleaner(mappings, response).clean()
    return dataset


class Mappings:

    def __init__(self, mapping_filepaths: dict):
        self._mapping_filepaths = mapping_filepaths
        self._load_location_map()
        self._load_missing_locations_map()
        self._load_employer_name_map()
        self._load_employer_industry_map()
        self._load_job_function_map()
        self._load_cont_ed_maps()
        self._load_jhu_degree_map()
        self._load_student_demographics_map()
        self._load_salary_map()
        self._load_outcome_map()
        self._load_fellowship_recoding_map()

    def _load_location_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['location'])
        self.location_map = ValueMapBuilder.build_cached_location_map(raw_data, 'raw_location')

    def _load_missing_locations_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['missing_locations'])
        self.missing_locations_map = ValueMapBuilder.build_location_map(raw_data, 'email')

    def _load_employer_name_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['employer_name'])
        self.employer_name_map = ValueMapBuilder.build_cached_value_map(raw_data, 'old_value', 'new_value')

    def _load_employer_industry_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['employer_industry'])
        self.employer_industry_map = ValueMapBuilder.build_cached_value_map(raw_data, 'employer', 'industry')

    def _load_job_function_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['job_function'])
        self.job_function_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'job_function')

    def _load_cont_ed_maps(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['cont_ed'])
        self.college_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'clean_college')
        self.major_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'clean_major')
        self.degree_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'degree')
        self.major_group_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'major_group')

    def _load_jhu_degree_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['jhu_degree'])
        self.jhu_degree_map = ValueMapBuilder.build_jhu_degree_map(raw_data)

    def _load_student_demographics_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['demographics'])
        self.gender_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'gender')
        self.first_gen_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'is_first_gen')
        self.pell_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'is_pell_eligible')
        self.urm_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'is_urm')
        self.visa_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'visa_status')

    def _load_salary_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['salary'])
        self.salary_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'salary')

    def _load_outcome_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['outcome'])
        self.outcome_map = ValueMapBuilder.build_value_map(raw_data, 'email', 'outcome')

    def _load_fellowship_recoding_map(self):
        raw_data = csv_to_list_of_dicts(self._mapping_filepaths['fellowship'])
        self.fellowship_recoding_map = ValueMapBuilder.build_multi_field_value_map(raw_data, 'email', {'fellowship_org', 'fellowship_name'})


class ResponseCleaner:

    def __init__(self, mappings: Mappings, response: SurveyResponse):
        self._response = response
        self._mappings = mappings

    def clean(self):
        self._clean_locations()
        self._add_missing_locations()
        self._set_is_jhu()
        self._clean_employer_names()
        self._clean_employer_industries()
        self._add_job_functions()
        self._clean_cont_ed_data()
        self._add_jhu_degree_info()
        self._add_student_demographic_info()
        self._clean_salary_values()
        self._clean_outcomes()
        self._recode_fellowships()

    def _clean_locations(self):
        self._response.metadata.location = self._mappings.location_map.get_mapping(self._response.metadata.location)

    def _add_missing_locations(self):
        try:
            self._response.metadata.location = self._mappings.missing_locations_map.get_mapping(self._response.student.email)
        except ValueMap.NoKnownMappingException:
            pass

    def _set_is_jhu(self):
        self._response.metadata.is_jhu = is_jhu(self._response.cont_ed.school) or is_jhu(self._response.employment.employer_name)

    def _clean_employer_names(self):
        self._response.employment.employer_name = self._mappings.employer_name_map.get_mapping(self._response.employment.employer_name)

    def _clean_employer_industries(self):
        try:
            self._response.employment.employer_industry = self._mappings.employer_industry_map.get_mapping(self._response.employment.employer_name)
        except ValueMap.NoKnownMappingException:
            pass

    def _add_job_functions(self):
        if self._response.metadata.outcome == 'Working':
            self._response.employment.job_function = self._mappings.job_function_map.get_mapping(self._response.student.email)

    def _clean_cont_ed_data(self):
        if self._response.metadata.outcome == 'Continuing Education':
            self._response.cont_ed.school = self._mappings.college_map.get_mapping(self._response.student.email)
            self._response.cont_ed.major = self._mappings.major_map.get_mapping(self._response.student.email)
            self._response.cont_ed.degree = self._mappings.degree_map.get_mapping(self._response.student.email)
            self._response.cont_ed.major_group = self._mappings.major_group_map.get_mapping(self._response.student.email)

    def _add_jhu_degree_info(self):
        self._response.student.jhu_degrees = self._mappings.jhu_degree_map.get_mapping(self._response.student.email)

    def _add_student_demographic_info(self):

        def _parse_bool(tf_str: str) -> Union[bool, None]:
            if tf_str == 'T':
                return True
            elif tf_str == 'F':
                return False
            elif not tf_str:
                return None
            else:
                raise ValueError(f'Cannot convert string "{tf_str}" to bool')

        self._response.student.gender = self._mappings.gender_map.get_mapping(self._response.student.email)
        self._response.student.is_first_gen = _parse_bool(self._mappings.first_gen_map.get_mapping(self._response.student.email))
        self._response.student.is_pell_eligible = _parse_bool(self._mappings.pell_map.get_mapping(self._response.student.email))
        self._response.student.is_urm = _parse_bool(self._mappings.urm_map.get_mapping(self._response.student.email))
        self._response.student.visa_status = self._mappings.visa_map.get_mapping(self._response.student.email)

    def _clean_salary_values(self):
        try:
            self._response.employment.salary = self._mappings.salary_map.get_mapping(self._response.student.email)
        except ValueMap.NoKnownMappingException:
            pass

    def _clean_outcomes(self):
        try:
            self._response.metadata.outcome = self._mappings.outcome_map.get_mapping(self._response.student.email)
        except ValueMap.NoKnownMappingException:
            pass

    def _recode_fellowships(self):
        try:
            recoding = self._mappings.fellowship_recoding_map.get_mapping(self._response.student.email)
            self._response.fellowship_data.fellowship_name = recoding['fellowship_name']
            self._response.fellowship_data.fellowship_org = recoding['fellowship_org']
            self._response.metadata.outcome = 'Fellowship'
        except ValueMap.NoKnownMappingException:
            pass
