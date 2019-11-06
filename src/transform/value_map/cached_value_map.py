from src.transform.value_map.value_map import ValueMap


class CachedValueMap(ValueMap):

    def __init__(self):
        super().__init__()
        self._clean_values = set()
        self._clean_values.add(None)

    def add_mapping(self, value, replacement):
        super().add_mapping(value, replacement)
        self._clean_values.add(replacement)

    def get_mapping(self, value):
        if value in self._clean_values:
            return value
        else:
            return self._get_mapping_for_unclean_value(value)

    def _get_mapping_for_unclean_value(self, value):
        try:
            return self._mapping[value]
        except KeyError:
            raise self.NoKnownMappingException(f'No known mapping for value "{value}"')
