from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.application.use_cases.start_test_session import StartTestSessionUseCase
from assessments.application.use_cases.save_candidate_answer import SaveCandidateAnswerUseCase
from assessments.application.use_cases.complete_test_session import CompleteTestSessionUseCase
from assessments.infrastructure.repositories.django_assessment_repository import DjangoAssessmentRepository


def _get_candidate_id(request):
    """Try to extract candidate ID from JWT cookie (optional)."""
    token = request.COOKIES.get("token")
    if not token:
        return None
    try:
        import jwt, environ
        env = environ.Env()
        payload = jwt.decode(token, env("JWT_SECRET"), algorithms=[env("JWT_ALGO")])
        from users.infrastructure.repositories.django_user_repository import DjangoUserRepository
        user = DjangoUserRepository().find_by_email(payload.get("sub"))
        return user.id if user else None
    except Exception:
        return None


class StartTestView(APIView):
    """
    POST /api/public/test/start/
    Body: { link_token }
    Returns: { session_id, questions, time_limit }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        link_token = request.data.get("link_token")
        if not link_token:
            return Response({"error": "link_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        candidate_id = _get_candidate_id(request)
        try:
            result = StartTestSessionUseCase(DjangoAssessmentRepository()).execute(
                link_token, candidate_id
            )
            return Response(result, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SubmitAnswerView(APIView):
    """
    POST /api/public/test/answer/
    Body: { session_id, question_id, question_type, answer_text }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        session_id = request.data.get("session_id")
        question_id = request.data.get("question_id")
        question_type = request.data.get("question_type")
        answer_text = request.data.get("answer_text", "")

        if not all([session_id, question_id, question_type]):
            return Response(
                {"error": "session_id, question_id, and question_type are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            from assessments.application.use_cases.save_candidate_answer import SaveCandidateAnswerUseCase
            result = SaveCandidateAnswerUseCase().execute(
                session_id, question_id, question_type, answer_text
            )
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CompleteTestView(APIView):
    """
    POST /api/public/test/complete/
    Body: { session_id }
    Returns: full result with per-question scores
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        session_id = request.data.get("session_id")
        if not session_id:
            return Response({"error": "session_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = CompleteTestSessionUseCase().execute(session_id)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
