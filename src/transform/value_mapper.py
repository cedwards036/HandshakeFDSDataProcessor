class ValueMapping:

    def __init__(self):
        self._mapping = {}

    def add_mapping(self, value, replacement):
        self._mapping[value] = replacement

    def get_mapping(self, value):
        try:
            return self._mapping[value]
        except KeyError:
            raise self.NoKnownMappingException(f'No known mapping for value "{value}"')

    class NoKnownMappingException(Exception):
        def __init__(self, message):
            super().__init__(message)
