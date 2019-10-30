class OtherOutcomesData:

    def __init__(self):
        self.still_looking_option = None
        self.not_seeking_option = None

    def to_dict(self) -> dict:
        return {
            'still_looking_option': self.still_looking_option,
            'not_seeking_option': self.not_seeking_option
        }

    def __eq__(self, other: 'OtherOutcomesData') -> bool:
        return self.to_dict() == other.to_dict()
