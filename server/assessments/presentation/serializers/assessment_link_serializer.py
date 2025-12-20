from rest_framework import serializers

class AssessmentLinkSerializer(serializers.Serializer):
    value = serializers.CharField(read_only=True)
    expiration = serializers.DateTimeField(read_only=True)