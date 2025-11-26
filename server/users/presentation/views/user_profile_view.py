import jwt
import environ

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.application.use_cases.get_user_profile import GetUserProfileUseCase
from users.infrastructure.repositories.django_user_repository import DjangoUserRepository
from users.presentation.serializers.user_serializer import UserSerializer

class UserProfileView(APIView):
    def get(self, request):
        # 1. Extract user_id from JWT cookie
        token = request.COOKIES.get('token')
        if not token:
            return Response({"error": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            env = environ.Env()
            payload = jwt.decode(token, env("JWT_SECRET"), algorithms=[env("JWT_ALGO")])
            email = payload.get('sub')
            
            # 2. Get user by email to get ID
            user_repository = DjangoUserRepository()
            user = user_repository.find_by_email(email)
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # 3. Call use case
            use_case = GetUserProfileUseCase(user_repository)
            profile = use_case.execute(user.id)
            
            # 4. Serialize and return
            serializer = UserSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)