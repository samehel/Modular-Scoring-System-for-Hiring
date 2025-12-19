from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.infrastructure.repositories.django_assessment_repository import DjangoAssessmentRepository
from assessments.presentation.middleware.auth_middleware import AuthMiddleware
from server.assessments.presentation.serializers.resume_assessment_serializer import ResumeAssessmentSerializer
from users.domain.value_objects.user_type import UserType

class AdminAssessmentListView(APIView):
    permission_classes = [AuthMiddleware(UserType.ADMIN)]

    def get(self, request):
        user = request.user_data
        try:
            assessment_repository = DjangoAssessmentRepository()
            assessments_list = assessment_repository.find_by_creator(user.id)
            
            serialized_list = ResumeAssessmentSerializer(assessments_list, many=True)

            response = Response({"assessments_list": serialized_list.data }, status=status.HTTP_200_OK)
            return response
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

