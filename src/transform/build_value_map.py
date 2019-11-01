from typing import List

from src.transform.value_map import ValueMap


def build_value_map(raw_mapping_data: List[dict], from_field: str, to_field: str) -> ValueMap:
    value_map = ValueMap()
    for row in raw_mapping_data:
        value_map.add_mapping(row[from_field], row[to_field])
    return value_map
