class UserProfileDto():
    def __init__(self, user_id: str, email: str, user_type: str, profile_data: dict, created_at: datetime):
        self.user_id = user_id
        self.email = email
        self.user_type = user_type
        self.profile_data = profile_data
        self.created_at = created_at
