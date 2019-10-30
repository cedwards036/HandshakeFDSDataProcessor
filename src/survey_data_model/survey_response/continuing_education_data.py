class ContinuingEducationData:

    def __init__(self):
        self.school = None
        self.level = None
        self.major = None
        self.major_group = None
        self.degree = None

    def to_dict(self):
        return {
            'cont_ed_school': self.school,
            'cont_ed_level': self.level,
            'cont_ed_degree': self.degree,
            'cont_ed_major': self.major,
            'cont_ed_major_group': self.major_group,
        }

    def __eq__(self, other: 'ContinuingEducationData') -> bool:
        return self.to_dict() == other.to_dict()
