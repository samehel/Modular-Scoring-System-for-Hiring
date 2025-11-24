from rest_framework import serializers

class CandidateRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone = serializers.CharField()
    date_of_birth = serializers.DateField()