from rest_framework import serializers

class AssessmentLinkSerializer(serializers.Serializer):
    token = serializers.CharField(source='value', read_only=True)
    expiration = serializers.DateTimeField(read_only=True)