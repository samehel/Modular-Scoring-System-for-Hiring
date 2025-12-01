
from assessments.domain.interfaces.assessment_repository import AssessmentRepository

class GetAssessmentByLinkUseCase():

    def __init__(self, assessment_repository: AssessmentRepository) -> None:
        self.assessment_repository = assessment_repository

    def execute(self, token: str):

        if token is None or token == "":
            raise ValueError("Token cannot be empty")

        assessment = self.assessment_repository.find_by_link_token(token)

        if assessment is None:
            raise ValueError("Invalid link")
        
        return assessment