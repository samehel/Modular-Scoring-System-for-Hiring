
from assessments.domain.entities.assessment_base import AssessmentBase
from assessments.domain.entities.resume_assessment import ResumeAssessment
from assessments.domain.interfaces.assessment_repository import AssessmentRepository
from assessments.domain.value_objects.link_token import LinkToken
from assessments.models import Assessment as AssessmentModel, AssessmentLink
from assessments.models import ResumeAssessment as ResumeAssessmentModel
from assessments.models import Criterion as CriterionModel
from assessments.domain.value_objects.assessment_type import AssessmentType
from users.models import User as UserModel
from datetime import datetime

class DjangoAssessmentRepository(AssessmentRepository):

    def _to_domain(self, assessment_model: AssessmentModel) -> AssessmentBase:
        # Fetch all criteria for this assessment
        criterion_models = CriterionModel.objects(assessment=str(assessment_model.id)).all()
        criteria = [self._criterion_to_domain(cm) for cm in criterion_models]
        
        if assessment_model.type == AssessmentType.RESUME:
            return ResumeAssessment(
                id=str(assessment_model.id),
                name=assessment_model.name,
                description=assessment_model.description,
                type=assessment_model.type,
                status=assessment_model.status,
                created_by=str(assessment_model.created_by.id),
                created_at=assessment_model.created_at,
                updated_at=assessment_model.updated_at,
                criteria=criteria
            )
        else:
            raise ValueError(f"Unsupported assessment type: {assessment.type}")    

    def _to_model(self, assessment: AssessmentBase) -> AssessmentModel:
        """Convert domain entity to MongoDB model"""
        if assessment.type == AssessmentType.RESUME:
            return ResumeAssessmentModel(
                id=str(assessment.id),
                name=assessment.name,
                description=assessment.description,
                type=assessment.type,
                status=assessment.status,
                created_by=UserModel.objects(id=assessment.created_by).first(),
                created_at=assessment.created_at,
                updated_at=assessment.updated_at
            )
        else:
            raise ValueError(f"Unsupported assessment type: {assessment.type}")

    def _criterion_to_domain(self, criterion_model: CriterionModel) -> Criterion:
        return Criterion(
            id=criterion_model.id,
            name=criterion_model.name,
            type=criterion_model.type,
            weight=criterion_model.weight,
            rules=criterion_model.rules
        )

    def _criterion_to_model(self, criterion: Criterion, assessment_id: str) -> CriterionModel:
        return CriterionModel(
            assessment=assessment_id,
            name=criterion.name,
            type=criterion.type,
            weight=criterion.weight,
            rules=criterion.rules
        )

    def save(self, assessment: AssessmentBase) -> AssessmentBase | None:
        new_assessment = self._to_model(assessment)
        saved_assessment = new_assessment.save()
        
        # Save criteria if ResumeAssessment
        if isinstance(assessment, ResumeAssessment) and assessment.criteria:
            for criterion in assessment.criteria:
                criterion_model = self._criterion_to_model(criterion, str(saved_assessment.id))
                criterion_model.save()
        
        return self._to_domain(saved_assessment) if saved_assessment else None
    
    def save_link(self, assessment_id: str, link_token: LinkToken) -> LinkToken:
        link_model = AssessmentLink(
            assessment=assessment_id,
            token=link_token.value,
            expiration=link_token.expiration
        )
        link_model.save()
        return LinkToken(
            value=link_model.token,
            expiration=link_model.expiration
        )

    def find_by_id(self, Id: str) -> AssessmentBase | None:
        foundAssessment = AssessmentModel.objects(id=Id).first()
        return self._to_domain(foundAssessment) if foundAssessment else None
    
    def find_by_link_token(self, linkToken: str) -> AssessmentBase | None:
        link_model = AssessmentLink.objects(token=linkToken).first()
        if not link_model:
            return None
        
        assessment_model = link_model.assessment
        return self._to_domain(assessment_model)
    
    def find_by_creator(self, creator: str) -> list[AssessmentBase] | None:
        user_model = UserModel.objects(id=creator).first()
        if not user_model:
            return None
        
        assessment_models = AssessmentModel.objects(created_by=user_model).all()
        if not assessment_models:
            return None
        
        assessments = [self._to_domain(assessment_model) for assessment_model in assessment_models]
        return assessments
    
    def update(self, assessment: AssessmentBase) -> AssessmentBase | None:
        assessment_model = AssessmentModel.objects(id=assessment.id).first()
        if not assessment_model:
            return None

        assessment_model.name = assessment.name
        assessment_model.description = assessment.description
        assessment_model.type = assessment.type
        assessment_model.status = assessment.status
        assessment_model.updated_at = datetime.now()
        assessment_model.save()
        
        # Update criteria if ResumeAssessment
        if isinstance(assessment, ResumeAssessment):
            # Delete existing criteria
            CriterionModel.objects(assessment=assessment.id).delete()
            # Save new criteria
            for criterion in assessment.criteria:
                criterion_model = self._criterion_to_model(criterion, assessment.id)
                criterion_model.save()
        
        return self._to_domain(assessment_model)

    def delete(self, Id: str) -> bool:
        # Delete all criteria first
        CriterionModel.objects(assessment=Id).delete()
        # Delete assessment
        deleted_count = AssessmentModel.objects(id=Id).delete()
        return deleted_count > 0
