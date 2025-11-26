from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.application.dtos.register_candidate_dto import RegisterCandidateDto
from users.application.use_cases.register_candidate import RegisterCandidateUseCase
from users.infrastructure.repositories.django_user_repository import DjangoUserRepository
from users.presentation.serializers.candidate_register_serializer import CandidateRegisterSerializer

class RegisterCandidateView(APIView):
    def post(self, request):

        # Parse request with serializer
        serializer = CandidateRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create our RegisterCandidateDTO
        dto = RegisterCandidateDto(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            phone=serializer.validated_data['phone'],
            date_of_birth=serializer.validated_data['date_of_birth']
        )

        # Call our use case
        try:
            user_repository = DjangoUserRepository()
            use_case = RegisterCandidateUseCase(user_repository)
            user = use_case.execute(dto)

            # Return our response
            return Response({
                "message": "Candidate Registered",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)