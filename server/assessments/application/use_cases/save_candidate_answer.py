"""Phase 9 — Save a candidate answer for an active test session."""
from assessments.models import TestSession, CandidateAnswer


class SaveCandidateAnswerUseCase:

    def execute(self, session_id: str, question_id: str,
                question_type: str, answer_text: str) -> dict:
        session = TestSession.objects(id=session_id).first()
        if not session:
            raise ValueError(f"Session {session_id} not found")
        if session.status != "IN_PROGRESS":
            raise ValueError("Session is no longer active")

        # Upsert: update if answer already exists for this question in session
        existing = CandidateAnswer.objects(session=session, question_id=question_id).first()
        if existing:
            existing.answer_text = answer_text
            existing.question_type = question_type
            existing.save()
        else:
            CandidateAnswer(
                session=session,
                question_id=question_id,
                question_type=question_type,
                answer_text=answer_text,
            ).save()

        return {"acknowledged": True, "session_id": session_id, "question_id": question_id}
