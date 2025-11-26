from users.domain.value_objects.email import Email
from users.models import User as UserModel
from users.domain.entities.user import User
from users.domain.interfaces.user_repository import UserRepository
from datetime import datetime

class DjangoUserRepository(UserRepository):

    def _to_domain(self, user_model: UserModel) -> User:
        """Convert MongoDB UserModel to domain User entity"""
        return User(
            id=str(user_model.id),
            email=Email(user_model.email),
            password_hash=user_model.password_hash,
            user_type=user_model.user_type,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )
    
    def _to_model(self, user: User) -> UserModel:
        """Convert domain User entity to MongoDB UserModel"""
        return UserModel(
            email=user.email.value,
            password_hash=user.password_hash,
            user_type=user.user_type,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    def save(self, user: User) -> User | None:
        newUser = self._to_model(user)
        savedUser = newUser.save()
        return self._to_domain(savedUser) if savedUser else None
    
    def find_by_email(self, email: str) -> User | None:
        foundUser = UserModel.objects(email=email).first()
        return self._to_domain(foundUser) if foundUser else None

    def find_by_id(self, Id: str) -> User | None:
        foundUser = UserModel.objects(id=Id).first()
        return self._to_domain(foundUser) if foundUser else None

    def update(self, user: User) -> User | None:
        userModel = UserModel.objects(id=user.id).first()
        if userModel:
            userModel.email = user.email.value
            userModel.password_hash = user.password_hash
            userModel.user_type = user.user_type
            userModel.updated_at = datetime.now()
            userModel.save()
            return self._to_domain(userModel)
        return None

    def delete(self, Id: str) -> bool:
        deleted_count = UserModel.objects(id=Id).delete()
        return deleted_count > 0