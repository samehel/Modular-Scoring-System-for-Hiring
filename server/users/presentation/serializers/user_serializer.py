from rest_framework import serializers
from users.domain.value_objects.user_type import UserType

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    user_type = serializers.ChoiceField(choices=[UserType.ADMIN, UserType.CANDIDATE])
    profile_data = serializers.DictField()
    created_at = serializers.DateTimeField(read_only=True)