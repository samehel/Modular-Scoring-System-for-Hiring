import uuid 

from assessments.domain.value_objects.assessment_type import AssessmentType
from assessments.domain.interfaces.assessment_repository import AssessmentRepository
from assessments.application.dtos.create_resume_assessment_dto import CreateResumeAssessmentDTO
from assessments.domain.entities.resume_assessment import ResumeAssessment
from assessments.domain.value_objects.assessment_status import AssessmentStatus
from users.domain.interfaces.user_repository import UserRepository
from datetime import datetime

class CreateResumeAssessmentUseCase():

    def __init__(self, assessment_repository: AssessmentRepository, user_repository: UserRepository) -> None:
        self.assessment_repository = assessment_repository
        self.user_repository = user_repository

    def execute(self, dto: CreateResumeAssessmentDTO, user_id: str):

        if dto.name is None or dto.name == "":
            raise ValueError("The name of the assessment cannot be empty")

        if dto.description is None or dto.description == "":
            raise ValueError("The description for the assessment cannot be empty")

        if user_id is None or user_id == "":
            raise ValueError("The author cannot be empty")

        user = self.user_repository.find_by_id(user_id)

        if user is None:
            raise ValueError("The author does not exist")

        resume = ResumeAssessment(
            id=str(uuid.uuid4()),
            name=dto.name,
            description=dto.description,
            type=AssessmentType.RESUME,
            status=AssessmentStatus.DRAFT,
            created_by=user.email.value.split("@")[0],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            criteria=[]
        )

        saved_resume = self.assessment_repository.save(resume)

        if saved_resume is None:
            raise ValueError("Failed to create a new resume assessment")
        
        return saved_resume