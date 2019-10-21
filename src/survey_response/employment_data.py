class EmploymentData:

    def __init__(self):
        self.employer_name = None
        self.employer_industry = None
        self.employment_category = None
        self.employment_type = None
        self.job_function = None
        self.job_title = None
        self.found_through_handshake = None
        self.employed_during_education = None
        self.offer_date = None
        self.accept_date = None
        self.start_date = None
        self.salary = None
        self.bonus_amount = None
        self.other_compensation = None
        self.is_internship = None

    def to_dict(self) -> dict:
        return {
            'employer_name': self.employer_name,
            'employer_industry': self.employer_industry,
            'employment_category': self.employment_category,
            'employment_type': self.employment_type,
            'job_function': self.job_function,
            'job_title': self.job_title,
            'found_through_handshake': self.found_through_handshake,
            'employed_during_education': self.employed_during_education,
            'offer_date': self.offer_date,
            'accept_date': self.accept_date,
            'start_date': self.start_date,
            'salary': self.salary,
            'bonus_amount': self.bonus_amount,
            'other_compensation': self.other_compensation,
            'is_internship': self.is_internship,
        }

    def __eq__(self, other: 'EmploymentData') -> bool:
        return self.to_dict() == other.to_dict()
