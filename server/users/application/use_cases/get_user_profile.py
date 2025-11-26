from users.application.dtos.user_profile_dto import UserProfileDto
from users.domain.interfaces.user_repository import UserRepository

class GetUserProfileUseCase():
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str) -> UserProfileDto:
        user = self.user_repository.find_by_id(user_id)
        # Check if user exists
        if user is None:
            raise ValueError("User Profile does not exist")
        
        user_profile = UserProfileDto(
            user_id=user.id,
            email=user.email.value,
            user_type=user.user_type.value,
            profile_data={},
            created_at=user.created_at
        )

        return user_profile


