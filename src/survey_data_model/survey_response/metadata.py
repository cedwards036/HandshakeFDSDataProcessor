from src.survey_data_model.survey_response.location import Location


class Metadata:

    def __init__(self):
        self.response_id = None
        self.response_datetime_utc = None
        self.outcome = None
        self.location = Location()
        self.is_jhu = None
        self.submitted_by = None
        self.is_knowledge_response = None
        self.knowledge_source = None

    def to_dict(self) -> dict:
        return {
            'response_id': self.response_id,
            'response_datetime_utc': self.response_datetime_utc,
            'outcome': self.outcome,
            'location': self.location.to_dict(),
            'is_jhu': self.is_jhu,
            'submitted_by': self.submitted_by,
            'is_knowledge_response': self.is_knowledge_response,
            'knowledge_source': self.knowledge_source
        }

    def __eq__(self, other: 'Metadata') -> bool:
        return self.to_dict() == other.to_dict()
