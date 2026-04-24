import uuid
from datetime import datetime
from typing import List, Optional

from assessments.domain.interfaces.result_repository import ResultRepository
from assessments.models import (
    AssessmentResult,
    ResumeData,
    ScoreBreakdown,
    Assessment as AssessmentModel,
    Criterion as CriterionModel,
)
from users.models import User as UserModel


class DjangoResultRepository(ResultRepository):
    """
    MongoEngine-backed implementation of ResultRepository.
    Stores AssessmentResult, ResumeData, and ScoreBreakdown documents.
    """

    def save_result(self, result_data: dict) -> dict:
        """
        Persist a new assessment result.

        result_data keys:
            assessment_id, candidate_id (optional), total_score,
            parsed_data, score_breakdown (list of dicts), submitted_at
        """
        assessment = AssessmentModel.objects(id=result_data["assessment_id"]).first()
        if not assessment:
            raise ValueError(f"Assessment {result_data['assessment_id']} not found")

        candidate = None
        if result_data.get("candidate_id"):
            candidate = UserModel.objects(id=result_data["candidate_id"]).first()

        result = AssessmentResult(
            assessment=assessment,
            candidate=candidate,
            total_score=result_data["total_score"],
            submitted_at=result_data.get("submitted_at", datetime.now()),
        )
        result.save()

        # Save parsed resume data
        resume_data = ResumeData(
            assessment_result=result,
            parsed_data=result_data.get("parsed_data", {}),
        )
        resume_data.save()

        # Save per-criterion score breakdown
        for entry in result_data.get("score_breakdown", []):
            criterion = CriterionModel.objects(id=entry.get("criterion_id")).first()
            breakdown = ScoreBreakdown(
                result=result,
                criterion=criterion,
                score=entry.get("score", 0.0),
            )
            breakdown.save()

        return self._serialize(result)

    def get_result_by_id(self, result_id: str) -> Optional[dict]:
        result = AssessmentResult.objects(id=result_id).first()
        if not result:
            return None
        return self._serialize_full(result)

    def get_results_for_assessment(self, assessment_id: str) -> List[dict]:
        assessment = AssessmentModel.objects(id=assessment_id).first()
        if not assessment:
            return []
        results = AssessmentResult.objects(assessment=assessment).order_by("-submitted_at")
        return [self._serialize(r) for r in results]

    def get_results_for_candidate(self, candidate_id: str) -> List[dict]:
        candidate = UserModel.objects(id=candidate_id).first()
        if not candidate:
            return []
        results = AssessmentResult.objects(candidate=candidate).order_by("-submitted_at")
        return [self._serialize_with_assessment(r) for r in results]

    # ── Private helpers ──────────────────────────────────────────────────────

    def _serialize(self, result: AssessmentResult) -> dict:
        return {
            "id": str(result.id),
            "assessment_id": str(result.assessment.id),
            "total_score": result.total_score,
            "submitted_at": result.submitted_at.isoformat(),
        }

    def _serialize_full(self, result: AssessmentResult) -> dict:
        base = self._serialize(result)

        resume_data = ResumeData.objects(assessment_result=result).first()
        base["parsed_data"] = resume_data.parsed_data if resume_data else {}

        breakdowns = ScoreBreakdown.objects(result=result).all()
        base["score_breakdown"] = [
            {
                "criterion_id": str(b.criterion.id) if b.criterion else None,
                "criterion_name": b.criterion.name if b.criterion else None,
                "score": b.score,
            }
            for b in breakdowns
        ]

        if result.candidate:
            base["candidate_id"] = str(result.candidate.id)

        return base

    def _serialize_with_assessment(self, result: AssessmentResult) -> dict:
        base = self._serialize(result)
        assessment = result.assessment
        base["assessment_name"] = assessment.name
        base["assessment_type"] = assessment.type
        base["assessment_status"] = assessment.status
        return base
