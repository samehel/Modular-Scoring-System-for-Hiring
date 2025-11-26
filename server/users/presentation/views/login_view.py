from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.application.dtos.login_dto import LoginDto
from users.application.use_cases.login_user import LoginUserUseCase
from users.infrastructure.repositories.django_user_repository import DjangoUserRepository
from users.presentation.serializers.login_serializer import LoginSerializer

class LoginView(APIView):
    def post(self, request):
        # 1. Parse request with serializer
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Create DTO
        dto = LoginDto(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )
        
        # 3. Call use case
        try:
            user_repository = DjangoUserRepository()
            use_case = LoginUserUseCase(user_repository)
            res = use_case.execute(dto)
            
            # 4. Return response and set our token in the cookie
            response = Response({"message": "Login Successful", "user_type": res['user_type']}, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='token',
                value=res['token'],
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=int(res['max_age']) * 60
            )
            return response
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)