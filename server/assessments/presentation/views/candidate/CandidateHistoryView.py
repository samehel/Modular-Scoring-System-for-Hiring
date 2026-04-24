from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.application.use_cases.get_candidate_history import GetCandidateHistoryUseCase
from assessments.infrastructure.repositories.django_result_repository import DjangoResultRepository
from assessments.presentation.middleware.auth_middleware import RequireUserType
from users.domain.value_objects.user_type import UserType


class CandidateHistoryView(APIView):
    """
    GET /api/candidate/history/

    Returns paginated list of all assessment results for the
    authenticated candidate user.
    """

    permission_classes = [RequireUserType(UserType.CANDIDATE)]

    def get(self, request):
        user = request.user_data
        try:
            use_case = GetCandidateHistoryUseCase(
                result_repository=DjangoResultRepository()
            )
            results = use_case.execute(user.id)

            # Simple pagination via query params
            try:
                page = int(request.query_params.get("page", 1))
                limit = int(request.query_params.get("limit", 10))
            except ValueError:
                page, limit = 1, 10

            start = (page - 1) * limit
            end = start + limit
            paginated = results[start:end]

            return Response(
                {
                    "total": len(results),
                    "page": page,
                    "limit": limit,
                    "results": paginated,
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
