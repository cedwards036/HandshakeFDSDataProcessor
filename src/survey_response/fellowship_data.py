class FellowshipData:

    def __init__(self):
        self.fellowship_org = None
        self.fellowship_name = None

    def to_dict(self) -> dict:
        return {
            'fellowship_org': self.fellowship_org,
            'fellowship_name': self.fellowship_name
        }

    def __eq__(self, other: 'FellowshipData') -> bool:
        return self.to_dict() == other.to_dict()
