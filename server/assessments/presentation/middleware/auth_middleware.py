from rest_framework.permissions import BasePermission
import jwt
import environ

class AuthMiddleware(BasePermission):
    def __init__(self, allowed_user_type):
        self.allowed_user_type = allowed_user_type
        super().__init__()
    
    def has_permission(self, request, view):
        token = request.COOKIES.get('token')
        if not token:
            return False
        
        try:
            env = environ.Env()
            payload = jwt.decode(token, env("JWT_SECRET"), algorithms=[env("JWT_ALGO")])
            email = payload.get('sub')
            
            from users.infrastructure.repositories.django_user_repository import DjangoUserRepository
            
            user_repository = DjangoUserRepository()
            user = user_repository.find_by_email(email)
            
            if (user is None):
                return False

            request.user_data = user
            
            return user and user.user_type == self.allowed_user_type
        except:
            return False