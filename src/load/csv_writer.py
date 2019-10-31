import csv
from typing import List


class CSVWriter:

    def __init__(self, data: List[dict]):
        self._data = data
        self._header = data[0].keys()

    def write(self, filepath: str):
        with open(filepath, 'w') as f:
            writer = csv.DictWriter(f, self._header, lineterminator='\n')
            writer.writeheader()
            writer.writerows(self._data)
