from typing import List

from src.survey_data_model.survey_response.location import Location
from src.transform.value_map import LocationMap


def build_location_map(raw_mapping_data: List[dict]) -> LocationMap:
    result = LocationMap()
    for row in raw_mapping_data:
        result.add_mapping(row['raw_location'], _build_location_from_row(row))
    return result


def _build_location_from_row(row: dict):
    return Location(row['city'], row['state'], row['country'])
