
class AssessmentLinkDTO():

    def __init__(self, assessment_id: str, expiration_days: int) -> None:
        self.assessment_id = assessment_id
        self.expiration_days = expiration_days