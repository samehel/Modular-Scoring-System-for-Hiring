from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.application.use_cases.submit_resume import SubmitResumeUseCase
from assessments.application.dtos.resume_submission_dto import ResumeSubmissionDTO
from assessments.infrastructure.repositories.django_assessment_repository import DjangoAssessmentRepository
from assessments.infrastructure.repositories.django_result_repository import DjangoResultRepository
from assessments.infrastructure.parsers.pdf_resume_parser import PDFResumeParser
from assessments.application.strategies.resume_scoring_strategy import ResumeScoringStrategy
from assessments.presentation.serializers.assessment_result_serializer import AssessmentResultSerializer


class SubmitResumeView(APIView):
    """
    Public endpoint — no authentication required.
    Accepts a PDF resume and a link token, scores the resume,
    persists the result, and returns the score breakdown.

    POST /api/public/submit/resume/
    Content-Type: multipart/form-data

    Fields:
        link_token  (str, required)
        resume      (file, required)
        name        (str, optional) — anonymous candidate display name
        email       (str, optional)
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        link_token = request.data.get("link_token")
        resume_file = request.FILES.get("resume")

        if not link_token:
            return Response(
                {"error": "link_token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not resume_file:
            return Response(
                {"error": "resume file is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Optional: associate with a logged-in candidate
        candidate_id = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = None

        if token:
            try:
                import jwt
                import environ
                env = environ.Env()
                payload = jwt.decode(token, env("JWT_SECRET"), algorithms=[env("JWT_ALGO")])
                email = payload.get("sub")
                from users.infrastructure.repositories.django_user_repository import DjangoUserRepository
                user_repo = DjangoUserRepository()
                user = user_repo.find_by_email(email)
                if user:
                    candidate_id = user.id
            except Exception:
                pass  # Anonymous submission — that is fine

        try:
            file_bytes = resume_file.read()
            dto = ResumeSubmissionDTO(
                link_token=link_token,
                file=file_bytes,
                candidate_id=candidate_id,
            )

            use_case = SubmitResumeUseCase(
                assessment_repository=DjangoAssessmentRepository(),
                result_repository=DjangoResultRepository(),
                parser=PDFResumeParser(),
                scoring_strategy=ResumeScoringStrategy(),
            )

            result = use_case.execute(dto)

            return Response(
                {
                    "message": "Resume submitted and scored successfully",
                    "result_id": result.result_id,
                    "total_score": result.total_score,
                    "scores": result.scores,
                    "parsed_data": result.parsed_data,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
