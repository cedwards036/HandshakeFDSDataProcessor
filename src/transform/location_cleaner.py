from src.survey_data_model.survey_response.location import Location
from src.transform.value_map import ValueMap


class LocationCleaner(ValueMap):

    def add_mapping(self, value: str, replacement: Location):
        super().add_mapping(value, replacement)

    def get_mapping(self, loc: Location) -> Location:
        return super().get_mapping(loc.full_location)
