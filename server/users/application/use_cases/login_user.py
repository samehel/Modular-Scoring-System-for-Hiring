
import bcrypt
import environ
import os
import jwt

from server.users.application.dtos.login_dto import LoginDto
from server.users.domain.interfaces.user_repository import UserRepository
from datetime import datetime, timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Import .env configuration file
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

class LoginUserUseCase():
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, dto: LoginDto) -> dict:
        user = self.user_repository.find_by_email(dto.email)

        # Check if the user exists and if the credentials entered are correct
        if not user or not bcrypt.checkpw(dto.password.encode('utf-8'), user.password_hash):
            raise ValueError("Invalid credentials")
        
        expire = datetime.now() + timedelta(minutes=int(env("JWT_EXPIRE_MINUTES")))
        token = jwt.encode({ "sub": user.email, "exp": expire }, env("JWT_SECRET"), algorithm=env("JWT_ALGO"))

        return { 
            "token": token,
            "user_type": user.user_type.value,
            "user_id": user.id
        }