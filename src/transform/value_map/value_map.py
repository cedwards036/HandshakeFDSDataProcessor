class ValueMap:

    def __init__(self):
        self._mapping = {}
        self._clean_values = set()
        self._clean_values.add(None)

    def add_mapping(self, value, replacement):
        self._mapping[value] = replacement
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

    class NoKnownMappingException(Exception):
        def __init__(self, message):
            super().__init__(message)

    def __eq__(self, other: 'ValueMap') -> bool:
        return self._mapping == other._mapping
