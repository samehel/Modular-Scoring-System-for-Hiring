from assessments.models import Criterion, Assessment
from bson import ObjectId


class DeleteCriterionUseCase:
    """Remove a criterion document and return the updated assessment dict."""

    def execute(self, assessment_id: str, criterion_id: str, admin_id: str) -> dict:
        try:
            assessment = Assessment.objects.get(id=assessment_id)
        except Assessment.DoesNotExist:
            raise ValueError("Assessment not found")

        # Ensure the requesting admin owns this assessment
        if str(assessment.created_by.id) != admin_id:
            raise PermissionError("You do not own this assessment")

        try:
            criterion = Criterion.objects.get(
                id=ObjectId(criterion_id),
                assessment=assessment,
            )
        except Criterion.DoesNotExist:
            raise ValueError("Criterion not found on this assessment")

        criterion.delete()

        # Return remaining criteria so the frontend can update its list
        remaining = Criterion.objects(assessment=assessment)
        return {
            "assessment_id": str(assessment.id),
            "criteria": [
                {
                    "id": str(c.id),
                    "name": c.name,
                    "type": c.type,
                    "weight": c.weight,
                    "rules": c.rules,
                }
                for c in remaining
            ],
        }

