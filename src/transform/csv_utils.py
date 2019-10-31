import csv
from typing import List


def csv_to_list_of_dicts(filepath: str) -> List[dict]:
    with open(filepath) as f:
        return [dict(row) for row in csv.DictReader(f, skipinitialspace=True)]
