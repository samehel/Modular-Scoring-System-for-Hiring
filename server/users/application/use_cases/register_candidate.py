import bcrypt
import uuid 

from server.users.application.dtos.register_candidate_dto import RegisterCandidateDto
from server.users.domain.entities.user import User
from server.users.domain.interfaces.user_repository import UserRepository
from server.users.domain.value_objects.email import Email
from server.users.domain.value_objects.user_type import UserType
from datetime import datetime, date

class RegisterCandidateUseCase():
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, dto: RegisterCandidateDto) -> User:
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
        if dto.phone is None or dto.phone == "":
            raise ValueError("Phone Number is required")

        # Industry Validation
        if dto.date_of_birth is None or not isinstance(dto.date_of_birth, date):
            raise ValueError("Date of birth is required")
        
        # Creating our User 
        user = User(
            id=str(uuid.uuid4()),
            email=validated_email,
            password_hash=bcrypt.hashpw(dto.password.encode('utf-8'), bcrypt.gensalt()),
            user_type=UserType.CANDIDATE,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        registeredUser = self.user_repository.save(user)

        # Check if it failed to create
        if registeredUser is None:
            raise ValueError("Failed to create new Candidate account.")
        
        return registeredUser

