from typing import List

from src.survey_data_model import JHUDegree
from src.survey_data_model import Location
from src.transform.value_map.cached_value_map import CachedValueMap
from src.transform.value_map.value_map import ValueMap


class _DegreeDataParser:

    def __init__(self, raw_mapping_data: List[dict]):
        self._raw_mapping_data = raw_mapping_data
        self._mapping_dict = {}

    def parse(self) -> dict:
        for row in self._raw_mapping_data:
            self._add_degree_data_to_mapping_dict(row)
        return self._mapping_dict

    def _add_degree_data_to_mapping_dict(self, row):
        jhu_degree = JHUDegree(degree=row['degree'], major=row['major'], college=row['college'])
        email = row['email']
        if email in self._mapping_dict:
            self._mapping_dict[email].append(jhu_degree)
        else:
            self._mapping_dict[email] = [jhu_degree]


class ValueMapBuilder:

    @staticmethod
    def build_value_map(raw_mapping_data: List[dict], from_field: str, to_field: str) -> ValueMap:
        return ValueMapBuilder._build_two_field_value_map(from_field, raw_mapping_data, to_field, ValueMap())

    @staticmethod
    def build_cached_value_map(raw_mapping_data: List[dict], from_field: str, to_field: str) -> CachedValueMap:
        return ValueMapBuilder._build_two_field_value_map(from_field, raw_mapping_data, to_field, CachedValueMap())

    @staticmethod
    def _build_two_field_value_map(from_field, raw_mapping_data, to_field, value_map):
        for row in raw_mapping_data:
            value_map.add_mapping(row[from_field], row[to_field])
        return value_map

    @staticmethod
    def build_cached_location_map(raw_mapping_data: List[dict], from_field: str) -> CachedValueMap:
        return ValueMapBuilder._populate_location_map(CachedValueMap(lambda loc: loc.full_location), raw_mapping_data, from_field)

    @staticmethod
    def build_location_map(raw_mapping_data: List[dict], from_field: str) -> ValueMap:
        return ValueMapBuilder._populate_location_map(ValueMap(), raw_mapping_data, from_field)

    @staticmethod
    def _populate_location_map(location_map, raw_mapping_data: List[dict], from_field: str):
        for row in raw_mapping_data:
            clean_location = Location(city=row['city'], state=row['state'], country=row['country'])
            raw_location = row[from_field]
            location_map.add_mapping(raw_location, clean_location)
        return location_map

    @staticmethod
    def build_jhu_degree_map(raw_mapping_data: List[dict]) -> ValueMap:
        result = ValueMap()
        mapping_dict = _DegreeDataParser(raw_mapping_data).parse()
        for email, degree_data in mapping_dict.items():
            result.add_mapping(email, degree_data)
        return result
