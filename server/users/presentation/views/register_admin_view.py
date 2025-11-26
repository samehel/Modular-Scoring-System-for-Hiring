from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.application.dtos.register_admin_dto import RegisterAdminDto
from users.application.use_cases.register_admin import RegisterAdminUseCase
from users.infrastructure.repositories.django_user_repository import DjangoUserRepository
from users.presentation.serializers.admin_register_serializer import AdminRegisterSerializer

class RegisterAdminView(APIView):
    def post(self, request):

        # Parse request with serializer
        serializer = AdminRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create our RegisterAdminDTO
        dto = RegisterAdminDto(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            company_name=serializer.validated_data['company_name'],
            industry=serializer.validated_data['industry']
        )

        # Call our use case
        try:
            user_repository = DjangoUserRepository()
            use_case = RegisterAdminUseCase(user_repository)
            user = use_case.execute(dto)

            # Return our response
            return Response({
                "message": "Admin Registered",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)