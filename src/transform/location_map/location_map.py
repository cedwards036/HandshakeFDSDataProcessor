from src.survey_data_model.survey_response.location import Location
from src.transform.value_map import ValueMap


class LocationMap(ValueMap):

    def add_mapping(self, value: str, replacement: Location):
        super().add_mapping(value, replacement)

    def get_mapping(self, loc: Location) -> Location:
        if loc in self._clean_values:
            return loc
        else:
            return self._get_mapping_for_unclean_value(loc.full_location)
