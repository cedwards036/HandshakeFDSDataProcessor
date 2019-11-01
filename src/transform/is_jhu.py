import re


def is_jhu(value: str) -> bool:
    if value and re.match(r'.*johns\s+hopkins.*', value.lower()) is not None:
        return True
    return False
