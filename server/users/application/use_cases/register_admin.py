import bcrypt
import uuid 

from server.users.application.dtos.register_admin_dto import RegisterAdminDto 
from server.users.domain.entities.user import User
from server.users.domain.interfaces.user_repository import UserRepository
from server.users.domain.value_objects.email import Email
from server.users.domain.value_objects.user_type import UserType
from datetime import datetime

class RegisterAdminUseCase():
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, dto: RegisterAdminDto) -> User:
        # Email Validations
        if dto.email is None or dto.email == "":
            raise ValueError("Email is required")

        validated_email = Email(dto.email)

        if not validated_email.validate():
            raise ValueError("Invalid email format")

        # Check if user already exists
        if isinstance(self.user_repository.find_by_email(dto.email), User):
            raise ValueError("User already exists")

        # Password Validations
        if dto.password is None or dto.password == "":
            raise ValueError("Password is required")

        # Company Validation
        if dto.company_name is None or dto.company_name == "":
            raise ValueError("Company name is required")

        # Industry Validation
        if dto.industry is None or dto.industry == "":
            raise ValueError("Industry is required")
        

        # Creating our User 
        user = User(
            id=str(uuid.uuid4()),
            email=validated_email,
            password_hash=bcrypt.hashpw(dto.password.encode('utf-8'), bcrypt.gensalt()),
            user_type=UserType.ADMIN,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        registeredUser = self.user_repository.save(user)

        # Check if it failed to create
        if registeredUser is None:
            raise ValueError("Failed to create new Admin account.")
        
        return registeredUser

