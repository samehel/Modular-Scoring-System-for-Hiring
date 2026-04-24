from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.application.use_cases.create_coding_assessment import CreateCodingAssessmentUseCase
from assessments.application.use_cases.create_interview_assessment import CreateInterviewAssessmentUseCase
from assessments.application.dtos.create_coding_assessment_dto import CreateCodingAssessmentDTO
from assessments.application.dtos.create_interview_assessment_dto import CreateInterviewAssessmentDTO
from assessments.infrastructure.repositories.django_assessment_repository import DjangoAssessmentRepository
from assessments.infrastructure.repositories.django_result_repository import DjangoResultRepository
from assessments.presentation.middleware.auth_middleware import RequireUserType
from users.domain.value_objects.user_type import UserType
from users.infrastructure.repositories.django_user_repository import DjangoUserRepository


class CreateCodingAssessmentView(APIView):
    """POST /api/admin/assessments/coding/create/"""
    permission_classes = [RequireUserType(UserType.ADMIN)]

    def post(self, request):
        user = request.user_data
        data = request.data
        try:
            dto = CreateCodingAssessmentDTO(
                name=data.get("name", ""),
                description=data.get("description", ""),
                topics=data.get("topics", []),
                difficulty=data.get("difficulty", "MEDIUM"),
                question_count=int(data.get("question_count", 5)),
                time_limit=int(data.get("time_limit", 60)),
            )
            result = CreateCodingAssessmentUseCase(
                DjangoAssessmentRepository(), DjangoUserRepository()
            ).execute(dto, user.id)
            return Response({"message": "Coding assessment created", "assessment": result},
                            status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateInterviewAssessmentView(APIView):
    """POST /api/admin/assessments/interview/create/"""
    permission_classes = [RequireUserType(UserType.ADMIN)]

    def post(self, request):
        user = request.user_data
        data = request.data
        try:
            dto = CreateInterviewAssessmentDTO(
                name=data.get("name", ""),
                description=data.get("description", ""),
                categories=data.get("categories", []),
                time_limit=int(data.get("time_limit", 45)),
                question_count=int(data.get("question_count", 5)),
            )
            result = CreateInterviewAssessmentUseCase(
                DjangoAssessmentRepository(), DjangoUserRepository()
            ).execute(dto, user.id)
            return Response({"message": "Interview assessment created", "assessment": result},
                            status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AssessmentResultsView(APIView):
    """GET /api/admin/assessments/<id>/results/"""
    permission_classes = [RequireUserType(UserType.ADMIN)]

    def get(self, request, assessment_id):
        try:
            page = int(request.query_params.get("page", 1))
            limit = int(request.query_params.get("limit", 10))
        except ValueError:
            page, limit = 1, 10

        results = DjangoResultRepository().get_results_for_assessment(assessment_id)
        start = (page - 1) * limit
        paginated = results[start: start + limit]
        return Response({"total": len(results), "page": page, "results": paginated})


class ResultDetailView(APIView):
    """GET /api/admin/results/<result_id>/"""
    permission_classes = [RequireUserType(UserType.ADMIN)]

    def get(self, request, result_id):
        result = DjangoResultRepository().get_result_by_id(result_id)
        if result is None:
            return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(result)


class AssessmentStatisticsView(APIView):
    """GET /api/admin/assessments/<assessment_id>/statistics/"""
    permission_classes = [RequireUserType(UserType.ADMIN)]

    def get(self, request, assessment_id):
        results = DjangoResultRepository().get_results_for_assessment(assessment_id)
        if not results:
            return Response({
                "submission_count": 0, "avg_score": 0, "min_score": 0,
                "max_score": 0, "pass_count": 0, "fail_count": 0,
            })

        scores = [r["total_score"] for r in results]
        pass_threshold = 50.0
        pass_count = sum(1 for s in scores if s >= pass_threshold)

        return Response({
            "submission_count": len(scores),
            "avg_score": round(sum(scores) / len(scores), 2),
            "min_score": round(min(scores), 2),
            "max_score": round(max(scores), 2),
            "pass_count": pass_count,
            "fail_count": len(scores) - pass_count,
            "pass_threshold": pass_threshold,
        })
