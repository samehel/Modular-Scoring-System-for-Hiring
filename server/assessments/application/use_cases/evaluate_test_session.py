"""
Phase 9 — Evaluate all answers in a completed test session.
Uses AnswerEvaluatorFactory to score each CandidateAnswer, then
persists an AssessmentResult with total_score.
"""
from datetime import datetime

from assessments.models import (
    TestSession, CandidateAnswer, AssessmentResult,
)
from assessments.infrastructure.factories.answer_evaluator_factory import AnswerEvaluatorFactory
from questions.models import Question as QuestionModel


class EvaluateTestSessionUseCase:

    def execute(self, session_id: str) -> dict:
        session = TestSession.objects(id=session_id).first()
        if not session:
            raise ValueError(f"Session {session_id} not found")

        answers = CandidateAnswer.objects(session=session).all()
        total_score = 0.0
        evaluated = []

        for answer in answers:
            q_model = QuestionModel.objects(id=answer.question_id).first()
            question_data = {}
            if q_model:
                question_data = {
                    "correct_answer": getattr(q_model, "correct_answer", None),
                    "test_cases": list(getattr(q_model, "test_cases", []) or []),
                    "keywords": list(getattr(q_model, "keywords", []) or []),
                    "choices": list(getattr(q_model, "choices", []) or []),
                }

            evaluator = AnswerEvaluatorFactory.get_evaluator(answer.question_type)
            result = evaluator.evaluate(answer.answer_text, question_data)

            answer.is_correct = result.get("is_correct")
            answer.score = result.get("score", 0.0)
            answer.save()

            total_score += answer.score
            evaluated.append({
                "question_id": answer.question_id,
                "score": answer.score,
                "is_correct": answer.is_correct,
                "feedback": result.get("feedback", ""),
            })

        # Normalise score to 0-100 based on number of questions
        num_answers = len(evaluated)
        average_score = (total_score / num_answers) if num_answers else 0.0

        # Persist AssessmentResult
        assessment_result = AssessmentResult(
            assessment=session.assessment,
            candidate=session.candidate,
            total_score=average_score,
            submitted_at=datetime.now(),
        )
        assessment_result.save()

        return {
            "result_id": str(assessment_result.id),
            "session_id": session_id,
            "total_score": average_score,
            "answers": evaluated,
        }
