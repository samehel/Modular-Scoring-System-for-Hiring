from rest_framework import serializers


class ResumeDataSerializer(serializers.Serializer):
    """Serializes the parsed sections of a resume."""
    education = serializers.CharField(allow_blank=True, default="")
    experience = serializers.CharField(allow_blank=True, default="")
    skills = serializers.CharField(allow_blank=True, default="")
    projects = serializers.CharField(allow_blank=True, default="")
    certifications = serializers.CharField(allow_blank=True, default="")
    summary = serializers.CharField(allow_blank=True, default="")
