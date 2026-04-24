"""
Phase 9 — Start Test Session use case.
Creates a TestSession record and returns the session ID + questions (without answers).
"""
import uuid
from datetime import datetime
from typing import Optional

from assessments.domain.interfaces.assessment_repository import AssessmentRepository
from assessments.models import TestSession, Assessment as AssessmentModel
from questions.models import Question as QuestionModel, MCQQuestion, CodingQuestion, TextQuestion


class StartTestSessionUseCase:

    def __init__(self, assessment_repository: AssessmentRepository) -> None:
        self.assessment_repository = assessment_repository

    def execute(self, link_token: str, candidate_id: Optional[str] = None) -> dict:
        # 1. Resolve assessment from link token
        assessment = self.assessment_repository.find_by_link_token(link_token)
        if assessment is None:
            raise ValueError("Invalid or expired assessment link token")

        # 2. Load question IDs from model
        from assessments.models import (
            CodingAssessment as CodingAssessmentModel,
            InterviewAssessment as InterviewAssessmentModel,
        )
        assessment_model = AssessmentModel.objects(id=assessment.id).first()
        question_ids = []
        time_limit = 60

        if hasattr(assessment_model, 'question_ids'):
            question_ids = list(assessment_model.question_ids or [])
        if hasattr(assessment_model, 'time_limit'):
            time_limit = assessment_model.time_limit

        # 3. Fetch questions (strip correct answers)
        questions = []
        for qid in question_ids:
            q = QuestionModel.objects(id=qid).first()
            if not q:
                continue
            q_data = {
                "id": str(q.id),
                "title": q.title,
                "description": q.description,
                "difficulty": q.difficulty,
                "topic": q.topic,
                "question_type": q.question_type,
            }
            if isinstance(q, MCQQuestion):
                q_data["choices"] = list(q.choices)
            elif isinstance(q, CodingQuestion):
                q_data["problem_statement"] = q.problem_statement
                # Strip solution code
            elif isinstance(q, TextQuestion):
                q_data["category"] = q.category
            questions.append(q_data)

        # 4. Create TestSession
        candidate_ref = None
        if candidate_id:
            from users.models import User as UserModel
            candidate_ref = UserModel.objects(id=candidate_id).first()

        session = TestSession(
            assessment=assessment_model,
            candidate=candidate_ref,
            start_time=datetime.now(),
            status="IN_PROGRESS",
        )
        session.save()

        return {
            "session_id": str(session.id),
            "assessment_id": str(assessment.id),
            "assessment_name": assessment.name,
            "questions": questions,
            "time_limit": time_limit,
        }
