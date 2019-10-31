from abc import ABC, abstractmethod


class CustomFormatter(ABC):

    @abstractmethod
    def format(self, data: dict) -> dict:
        pass


class NullCustomFormatter(CustomFormatter):

    def format(self, data: dict) -> dict:
        return data


class FDS2019CustomFormatter(CustomFormatter):

    def format(self, data: dict) -> dict:
        self._data = data
        self._flatten_activity('internships')
        self._flatten_activity('research')
        return self._data

    def _flatten_activity(self, activity):
        for field in self._data[activity]:
            self._data[f'{activity}_{field}'] = self._data[activity][field]
        del self._data[activity]
        del self._data[f'{activity}_name']
