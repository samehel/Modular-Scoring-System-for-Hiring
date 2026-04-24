from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.infrastructure.repositories.django_result_repository import DjangoResultRepository
from assessments.models import AssessmentResult
from users.domain.value_objects.user_type import UserType
from assessments.presentation.middleware.auth_middleware import RequireUserType

class ClaimResultView(APIView):
    """
    Allows a candidate to claim an anonymously submitted result 
    by providing the result ID.
    
    POST /api/candidate/results/claim/
    {
        "result_id": "string"
    }
    """
    permission_classes = [RequireUserType(UserType.CANDIDATE)]

    def post(self, request):
        result_id = request.data.get("result_id")
        if not result_id:
            return Response({"error": "result_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = AssessmentResult.objects(id=result_id).first()
            if not result:
                return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Don't allow reclaiming if it already belongs to someone else
            if result.candidate and str(result.candidate.id) != str(request.user_data.id):
                return Response({"error": "Result already claimed"}, status=status.HTTP_403_FORBIDDEN)
            
            result.candidate = request.user_data
            result.save()
            
            return Response({"message": "Result claimed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
