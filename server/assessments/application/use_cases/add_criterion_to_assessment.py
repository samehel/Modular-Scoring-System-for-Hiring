
from assessments.domain.interfaces.assessment_repository import AssessmentRepository
from assessments.application.dtos.criterion_dto import CriterionDTO
from assessments.domain.entities.criterion import Criterion
from assessments.domain.value_objects.criterion_type import CriterionType
from assessments.domain.entities.resume_assessment import ResumeAssessment

class AddCriterionToAssessmentUseCase():

    def __init__(self, assessment_repository: AssessmentRepository) -> None:
        self.assessment_repository = assessment_repository

    def execute(self, assessment_id: str, dto: CriterionDTO):

        if assessment_id is None or assessment_id == "":
            raise ValueError("Assessment ID cannot be empty")
        
        if dto.name is None or dto.name == "":
            raise ValueError("The name of the criterion cannot be empty")

        if dto.rules is None or len(dto.rules) == 0:
            raise ValueError("Rules have not been set for the criterion")
        
        if dto.type is None or dto.type not in [ct.value for ct in CriterionType]:
            raise ValueError("This criterion type does not exist")

        if dto.weight is None or dto.weight is 0.0:
            raise ValueError("Criterion weight cannot be 0")
        
        assessment = self.assessment_repository.find_by_id(assessment_id)

        if assessment is None:
            raise ValueError("Criterion cannot be added to an assessment that does not exist")

        if not isinstance(assessment, ResumeAssessment):
            raise ValueError("Criterions can only be added to Resumes")

        criterion = Criterion(
            name=dto.name,
            type=dto.type,
            weight=dto.weight,
            rules=dto.rules
        )

        assessment.criteria.append(criterion)

        updated_assessment = self.assessment_repository.update(assessment)

        if updated_assessment is None:
            raise ValueError("Failed to add criterion to resume")
        
        return updated_assessment
