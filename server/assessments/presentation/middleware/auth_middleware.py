from rest_framework.permissions import BasePermission
import jwt
import environ

def RequireUserType(user_type):
    class AuthMiddleware(BasePermission):
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
                
                if user is None:
                    return False

                request.user_data = user
                
                return user.user_type == user_type
            except:
                return False
    
    return AuthMiddleware