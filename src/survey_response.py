from typing import Union


class IntResponse:

    def __init__(self, value: Union[int, None]):
        self._value = value

    def __add__(self, other):
        return self._add(other)

    def __radd__(self, other):
        return self._add(other)

    def _add(self, other):
        if self._value == None:
            return other
        else:
            return self._value + other


class SurveyResponse:

    def __init__(self):
        self._data = {
            'response_id': None,
            'username': None,
            'jhed': None,
            'full_name': None,
            'jhu_colleges': [],
            'jhu_majors': [],
            'gender': None,
            'visa_status': None,
            'response_datetime_utc': None,
            'outcome': None,
            'employer_name': None,
            'employer_industry': None,
            'employment_category': None,
            'employment_type': None,
            'job_function': None,
            'job_title': None,
            'found_through_handshake': None,
            'employed_during_education': None,
            'offer_date': None,
            'accept_date': None,
            'start_date': None,
            'salary': None,
            'bonus_amount': None,
            'other_compensation': None,
            'is_authorized_to_work_in_us': None,
            'is_internship': None,
            'cont_ed_school': None,
            'cont_ed_level': None,
            'cont_ed_degree': None,
            'cont_ed_major': None,
            'cont_ed_major_group': None,
            'fellowship_org': None,
            'fellowship_name': None,
            'still_seeking_option': None,
            'not_seeking_option': None,
            'city': None,
            'state': None,
            'country': None,
            'is_jhu': None,
            'submitted_by': None,
            'is_knowledge_response': None,
            'knowledge_source': None,
            'is_gap_year': None,
            'unpaid_internships_count': IntResponse(None),
            'paid_internships_count': IntResponse(None),
            'all_internships_count': None,
            'unpaid_research_count': IntResponse(None),
            'paid_research_count': IntResponse(None),
            'all_research_count': None
        }

    @property
    def username(self) -> str:
        return self._data['username']

    @username.setter
    def username(self, new_username: str):
        self._data['username'] = new_username

    @property
    def unpaid_internships_count(self) -> int:
        return self._data['unpaid_internships_count']

    @unpaid_internships_count.setter
    def unpaid_internships_count(self, count: int):
        self._data['unpaid_internships_count'] = count
        self._update_all_internships_count()

    @property
    def paid_internships_count(self) -> int:
        return self._data['paid_internships_count']

    @paid_internships_count.setter
    def paid_internships_count(self, count: int):
        self._data['paid_internships_count'] = count
        self._update_all_internships_count()

    @property
    def all_internships_count(self) -> int:
        return self._data['all_internships_count']

    def _update_all_internships_count(self):
        self._data['all_internships_count'] = self._data['unpaid_internships_count'] + self._data['paid_internships_count']

    @property
    def unpaid_research_count(self) -> int:
        return self._data['unpaid_research_count']

    @unpaid_research_count.setter
    def unpaid_research_count(self, count: int):
        self._data['unpaid_research_count'] = count
        self._update_all_research_count()

    @property
    def paid_research_count(self) -> int:
        return self._data['paid_research_count']

    @paid_research_count.setter
    def paid_research_count(self, count: int):
        self._data['paid_research_count'] = count
        self._update_all_research_count()

    @property
    def all_research_count(self) -> int:
        return self._data['all_research_count']

    def _update_all_research_count(self):
        self._data['all_research_count'] = self._data['unpaid_research_count'] + self._data['paid_research_count']
