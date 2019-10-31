class Location:

    def __init__(self, city: str = None, state: str = None, country: str = None):
        self._data = [self._convert_empty_str_to_none(city),
                      self._convert_empty_str_to_none(state),
                      self._convert_empty_str_to_none(country)]

    @property
    def city(self) -> str:
        return self._data[0]

    @city.setter
    def city(self, new_city: str):
        self._data[0] = self._convert_empty_str_to_none(new_city)

    @staticmethod
    def _convert_empty_str_to_none(value: str):
        if value == '':
            return None
        else:
            return value

    @property
    def state(self) -> str:
        return self._data[1]

    @state.setter
    def state(self, new_state: str):
        self._data[1] = self._convert_empty_str_to_none(new_state)

    @property
    def country(self) -> str:
        return self._data[2]

    @country.setter
    def country(self, new_country: str):
        self._data[2] = self._convert_empty_str_to_none(new_country)

    @property
    def full_location(self) -> str:
        result = ''
        for value in self._data:
            if value:
                result += self._format_value(result, value)
        return result

    @staticmethod
    def _format_value(result, value) -> str:
        if not result:
            return value
        else:
            return f', {value}'

    def to_dict(self):
        return {
            'city': self._data[0],
            'state': self._data[1],
            'country': self._data[2]
        }

    def __eq__(self, other: 'Location'):
        return self.to_dict() == other.to_dict()

    def __hash__(self):
        return hash((self.city, self.state, self.country))
