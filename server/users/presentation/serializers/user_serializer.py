from rest_framework import serializers
from server.users.domain.value_objects.user_type import UserType

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    user_type = serializers.ChoiceField(choices=[UserType.ADMIN, UserType.CANDIDATE])
    created_at = serializers.DateTimeField(read_only=True)