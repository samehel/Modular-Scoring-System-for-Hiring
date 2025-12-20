from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.infrastructure.repositories.django_assessment_repository import DjangoAssessmentRepository
from assessments.presentation.middleware.auth_middleware import RequireUserType
from assessments.application.dtos.assessment_link_dto import AssessmentLinkDTO
from assessments.application.use_cases.generate_assessment_link import GenerateAssessmentLinkUseCase
from assessments.presentation.serializers.assessment_link_serializer import AssessmentLinkSerializer
from users.domain.value_objects.user_type import UserType

class GenerateLinkView(APIView):
    permission_classes = [RequireUserType(UserType.ADMIN)]

    def post(self, request, id):
        try:

            expiration_days = request.data.get("expiration_days")
            if not expiration_days:
                return Response({"error": "expiration_days is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            dto = AssessmentLinkDTO(
                assessment_id=id,
                expiration_days=expiration_days
            )

            assessment_repository = DjangoAssessmentRepository()
            use_case = GenerateAssessmentLinkUseCase(assessment_repository)
            res = use_case.execute(dto)
            
            serializer = AssessmentLinkSerializer(res)
            response = Response({"message": "Resume Assessment Link Successfully Generated", "assessment_link": serializer.data }, status=status.HTTP_201_CREATED)
            return response
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
