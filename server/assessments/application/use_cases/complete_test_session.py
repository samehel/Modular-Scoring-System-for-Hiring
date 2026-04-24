"""Phase 9 — Complete a test session and trigger evaluation."""
from datetime import datetime

from assessments.models import TestSession
from assessments.application.use_cases.evaluate_test_session import EvaluateTestSessionUseCase


class CompleteTestSessionUseCase:

    def execute(self, session_id: str) -> dict:
        session = TestSession.objects(id=session_id).first()
        if not session:
            raise ValueError(f"Session {session_id} not found")
        if session.status == "COMPLETED":
            raise ValueError("Session is already completed")

        session.status = "COMPLETED"
        session.end_time = datetime.now()
        session.save()

        # Evaluate all answers and return final result
        return EvaluateTestSessionUseCase().execute(session_id)
