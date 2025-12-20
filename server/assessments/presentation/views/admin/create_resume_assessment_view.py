from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assessments.presentation.serializers.resume_assessment_serializer import ResumeAssessmentSerializer
from assessments.infrastructure.repositories.django_assessment_repository import DjangoAssessmentRepository
from assessments.application.use_cases.create_resume_assessment import CreateResumeAssessmentUseCase
from assessments.presentation.middleware.auth_middleware import RequireUserType
from users.domain.value_objects.user_type import UserType
from users.infrastructure.repositories.django_user_repository import DjangoUserRepository
from assessments.application.dtos.create_resume_assessment_dto import CreateResumeAssessmentDTO

class CreateResumeAssessmentView(APIView):
    permission_classes = [RequireUserType(UserType.ADMIN)]

    def post(self, request):
        user = request.user_data
        try:
            serializer = ResumeAssessmentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            dto = CreateResumeAssessmentDTO(
                name=serializer.validated_data["name"],
                description=serializer.validated_data["description"]
            )

            user_repository = DjangoUserRepository()
            assessment_repository = DjangoAssessmentRepository()
            use_case = CreateResumeAssessmentUseCase(assessment_repository, user_repository)
            res = use_case.execute(dto, user.id)
            
            serializer = ResumeAssessmentSerializer(res)
            response = Response({"message": "Resume Assessment Successfully Created!", "assessment": serializer.data }, status=status.HTTP_201_CREATED)
            return response
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
