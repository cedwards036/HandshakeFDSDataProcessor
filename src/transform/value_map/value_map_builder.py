from typing import List

from src.survey_data_model import Location
from src.transform.value_map.cached_value_map import CachedValueMap
from src.transform.value_map.location_map import LocationMap
from src.transform.value_map.value_map import ValueMap


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
    def build_location_map(raw_mapping_data: List[dict]) -> LocationMap:
        result = LocationMap()
        for row in raw_mapping_data:
            result.add_mapping(row['raw_location'], Location(row['city'], row['state'], row['country']))
        return result
