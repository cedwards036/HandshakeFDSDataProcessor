from src.survey_data_model import Location
from src.transform.value_map.cached_value_map import CachedValueMap


class LocationMap(CachedValueMap):

    def get_mapping(self, loc: Location) -> Location:
        if loc in self._clean_values:
            return loc
        else:
            return self._get_mapping_for_unclean_value(loc.full_location)
