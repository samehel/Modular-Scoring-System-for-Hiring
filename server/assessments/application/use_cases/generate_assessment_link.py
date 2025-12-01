from datetime import datetime, timedelta
import secrets

from assessments.domain.interfaces.assessment_repository import AssessmentRepository
from assessments.application.dtos.assessment_link_dto import AssessmentLinkDTO
from assessments.domain.value_objects.link_token import LinkToken

class GenerateAssessmentLinkUseCase():

    def __init__(self, assessment_repository: AssessmentRepository) -> None:
        self.assessment_repository = assessment_repository

    def execute(self, dto: AssessmentLinkDTO):

        if dto.assessment_id is None or dto.assessment_id == "":
            raise ValueError("Assessment ID cannot be empty")

        if dto.expiration_days is None or dto.expiration_days is 0:
            raise ValueError("To generate a link, the days till expiry need to be > 0")
        
        link_token = LinkToken(
            value=secrets.token_urlsafe(32),
            expiration=datetime.now() + timedelta(days=dto.expiration_days)
        )

        saved_link_token = self.assessment_repository.save_link(dto.assessment_id, link_token)

        if saved_link_token is None:
            raise ValueError("Failed to create a new link for the assessment")
        
        return saved_link_token