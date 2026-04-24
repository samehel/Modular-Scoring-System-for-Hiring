import uuid
from datetime import datetime
from typing import Optional

from assessments.domain.interfaces.assessment_repository import AssessmentRepository
from assessments.domain.interfaces.resume_parser import ResumeParser
from assessments.domain.interfaces.scoring_strategy import ScoringStrategy
from assessments.application.dtos.resume_submission_dto import ResumeSubmissionDTO
from assessments.application.dtos.resume_result_dto import ResumeResultDTO


class SubmitResumeUseCase:
    """
    Orchestrates the resume submission flow:
    1. Validates the link token and retrieves the assessment
    2. Parses the uploaded resume file
    3. Scores the resume against all assessment criteria
    4. Persists the result
    5. Returns a ResumeResultDTO
    """

    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        result_repository,
        parser: ResumeParser,
        scoring_strategy: ScoringStrategy,
    ) -> None:
        self.assessment_repository = assessment_repository
        self.result_repository = result_repository
        self.parser = parser
        self.scoring_strategy = scoring_strategy

    def execute(self, dto: ResumeSubmissionDTO) -> ResumeResultDTO:
        # 1. Resolve assessment from link token
        assessment = self.assessment_repository.find_by_link_token(dto.link_token)
        if assessment is None:
            raise ValueError("Invalid or expired assessment link token")

        # 2. Parse resume
        parsed_data = self.parser.parse(dto.file)

        # 3. Score against criteria
        criteria = assessment.criteria  # List[Criterion]
        if not criteria:
            raise ValueError("Assessment has no scoring criteria defined")

        # Build per-criterion scores
        score_details = []
        total_score = 0.0

        for criterion in criteria:
            individual_score = self.scoring_strategy.score(parsed_data, [criterion])
            score_details.append({
                "criterion_id": str(criterion.id),
                "criterion_name": criterion.name,
                "score": individual_score,
                "max_score": criterion.weight * 100,
            })
            total_score += individual_score

        # 4. Persist result
        result_data = {
            "assessment_id": str(assessment.id),
            "candidate_id": dto.candidate_id,
            "total_score": total_score,
            "parsed_data": parsed_data,
            "score_breakdown": score_details,
            "submitted_at": datetime.now(),
        }
        saved_result = self.result_repository.save_result(result_data)

        # 5. Return DTO
        return ResumeResultDTO(
            result_id=saved_result.get("id"),
            parsed_data=parsed_data,
            scores=score_details,
            total_score=total_score,
        )
