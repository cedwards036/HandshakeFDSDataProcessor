from typing import Union


class JHUDegree:

    def __init__(self, degree: Union[str, None], major: Union[str, None], college: Union[str, None]):
        self.degree = degree
        self.major = major
        self.college = college

    def __eq__(self, other: 'JHUDegree') -> bool:
        try:
            return (self.degree == other.degree) and \
                   (self.major == other.major) and \
                   (self.college == other.college)
        except AttributeError:
            return False
