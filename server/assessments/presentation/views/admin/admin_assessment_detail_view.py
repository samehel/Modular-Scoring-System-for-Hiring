from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.infrastructure.repositories.django_assessment_repository import DjangoAssessmentRepository
from assessments.presentation.middleware.auth_middleware import RequireUserType
from assessments.presentation.serializers.resume_assessment_serializer import ResumeAssessmentSerializer
from users.domain.value_objects.user_type import UserType


class AdminAssessmentDetailView(APIView):
    permission_classes = [RequireUserType(UserType.ADMIN)]

    def get(self, request, assessment_id):
        try:
            assessment_repository = DjangoAssessmentRepository()
            assessment = assessment_repository.find_by_id(assessment_id)

            if not assessment:
                return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)

            # Ensure requesting admin owns this assessment
            if str(assessment.created_by) != str(request.user_data.id):
                return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

            serializer = ResumeAssessmentSerializer(assessment)
            return Response({"assessment": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
