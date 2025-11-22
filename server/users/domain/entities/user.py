from datetime import datetime
from users.domain.value_objects.email import Email
from users.domain.value_objects.user_type import UserType

class User():
    id: str
    email: Email
    password_hash: str
    user_type: UserType
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: str, email: Email, password_hash: str, user_type: UserType, created_at: datetime, updated_at: datetime):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.user_type = user_type
        self.created_at = created_at
        self.updated_at = updated_at
