from rest_framework import serializers

class AssessmentLinkSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)
    expiration = serializers.DateTimeField()