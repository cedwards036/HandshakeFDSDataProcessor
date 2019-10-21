import csv
from typing import List


def read_csv(filepath: str) -> List[dict]:
    with open(filepath, encoding='utf-8') as f:
        return [{k: v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]
