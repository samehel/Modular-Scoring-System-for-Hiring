from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.presentation.serializers.resume_assessment_serializer import ResumeAssessmentSerializer
from assessments.infrastructure.repositories.django_assessment_repository import DjangoAssessmentRepository
from assessments.presentation.middleware.auth_middleware import AuthMiddleware
from assessments.presentation.serializers.criterion_serializer import CriterionSerializer
from assessments.application.use_cases.add_criterion_to_assessment import AddCriterionToAssessmentUseCase
from users.domain.value_objects.user_type import UserType
from assessments.application.dtos.criterion_dto import CriterionDTO

class AddCriterionView(APIView):
    permission_classes = [AuthMiddleware(UserType.ADMIN)]

    def post(self, request, id):
        try:
            serializer = CriterionSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            dto = CriterionDTO(
                name=serializer.validated_data["name"],
                type=serializer.validated_data["type"],
                weight=serializer.validated_data["weight"],
                rules=serializer.validated_data["rules"]
            )

            assessment_repository = DjangoAssessmentRepository()
            use_case = AddCriterionToAssessmentUseCase(assessment_repository)
            res = use_case.execute(id, dto)
            
            serializer = ResumeAssessmentSerializer(res)
            response = Response({"message": "Criterion Successfully Added to Resume Assessment!", "assessment": serializer.data }, status=status.HTTP_201_CREATED)
            return response
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
