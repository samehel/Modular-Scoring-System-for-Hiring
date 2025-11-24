from rest_framework import serializers

class AdminRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    company_name = serializers.CharField()
    industry = serializers.CharField()