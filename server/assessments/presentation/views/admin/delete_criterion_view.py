from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.application.use_cases.delete_criterion import DeleteCriterionUseCase
from assessments.presentation.middleware.auth_middleware import RequireUserType
from users.domain.value_objects.user_type import UserType


class DeleteCriterionView(APIView):
    permission_classes = [RequireUserType(UserType.ADMIN)]

    def delete(self, request, assessment_id, criterion_id):
        try:
            admin_id = request.user_data.get("user_id")
            use_case = DeleteCriterionUseCase()
            result = use_case.execute(assessment_id, criterion_id, admin_id)
            return Response(
                {"message": "Criterion deleted", "criteria": result["criteria"]},
                status=status.HTTP_200_OK,
            )
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
