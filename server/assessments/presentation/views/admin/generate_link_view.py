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
            # Default to 30 days if not specified
            expiration_days = request.data.get("expiration_days", 30)

            dto = AssessmentLinkDTO(
                assessment_id=id,
                expiration_days=int(expiration_days)
            )

            assessment_repository = DjangoAssessmentRepository()
            use_case = GenerateAssessmentLinkUseCase(assessment_repository)
            res = use_case.execute(dto)

            serializer = AssessmentLinkSerializer(res)
            return Response(
                {"message": "Assessment link generated successfully", "link": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
