class StudentData:

    def __init__(self):
        self.username = None
        self.email = None
        self.jhed = None
        self.full_name = None
        self.jhu_colleges = None
        self.jhu_majors = None
        self.gender = None
        self.visa_status = None
        self.is_authorized_to_work_in_us = None

    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'email': self.email,
            'jhed': self.jhed,
            'full_name': self.full_name,
            'jhu_colleges': self.jhu_colleges,
            'jhu_majors': self.jhu_majors,
            'gender': self.gender,
            'visa_status': None,
            'is_authorized_to_work_in_us': self.is_authorized_to_work_in_us
        }

    def __eq__(self, other: 'StudentData') -> bool:
        return self.to_dict() == other.to_dict()
