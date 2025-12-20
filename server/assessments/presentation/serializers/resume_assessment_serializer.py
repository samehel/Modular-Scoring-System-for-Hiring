from rest_framework import serializers
from assessments.presentation.serializers.criterion_serializer import CriterionSerializer

class ResumeAssessmentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    type = serializers.ReadOnlyField(default="RESUME", read_only=True)
    status = serializers.CharField(read_only=True)
    criteria = CriterionSerializer(read_only=True, many=True)
    created_by = serializers.CharField(read_only=True)
    created_by_name = serializers.SerializerMethodField(read_only=True) 
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    

    def get_created_by_name(self, obj):
        from users.infrastructure.repositories.django_user_repository import DjangoUserRepository
        repo = DjangoUserRepository()
        user = repo.find_by_id(obj.created_by)
        return user.email.value.split("@")[0] if user else "Unknown"
