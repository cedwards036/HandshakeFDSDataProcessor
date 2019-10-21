from typing import List

from src.survey_response import SurveyResponse


class ResponseDataset:

    def __init__(self):
        self._responses = []
        self._responses_by_username = {}

    def add_response(self, response: SurveyResponse):
        self._responses.append(response)
        self._responses_by_username[response.username] = response

    def get_response_by_username(self, username: str):
        try:
            return self._responses_by_username[username]
        except KeyError:
            raise self.InvalidUsernameException(f'Username "{username}" is not in the dataset')

    class InvalidUsernameException(Exception):
        def __init__(self, message: str):
            super().__init__(message)

    def to_list_of_dict(self) -> List[dict]:
        return [response.to_dict() for response in self._responses]

    def __eq__(self, other: 'ResponseDataset') -> bool:
        return self.to_list_of_dict() == other.to_list_of_dict()
