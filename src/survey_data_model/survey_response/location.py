class Location:

    def __init__(self, city: str = None, state: str = None, country: str = None):
        self._data = [city, state, country]

    @property
    def city(self) -> str:
        return self._data[0]

    @city.setter
    def city(self, new_city: str):
        self._data[0] = new_city

    @property
    def state(self) -> str:
        return self._data[1]

    @state.setter
    def state(self, new_state: str):
        self._data[1] = new_state

    @property
    def country(self) -> str:
        return self._data[2]

    @country.setter
    def country(self, new_country: str):
        self._data[2] = new_country

    @property
    def full_location(self) -> str:
        result = ''
        for value in self._data:
            if value:
                if not result:
                    result = value
                else:
                    result += f', {value}'
        return result

    def to_dict(self):
        return {
            'city': self._data[0],
            'state': self._data[1],
            'country': self._data[2]
        }

    def __eq__(self, other: 'Location'):
        return self.to_dict() == other.to_dict()
