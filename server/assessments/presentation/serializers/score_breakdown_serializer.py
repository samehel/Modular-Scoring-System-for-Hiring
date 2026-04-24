from rest_framework import serializers


class ScoreBreakdownSerializer(serializers.Serializer):
    """Serializes one criterion's score entry."""
    criterion_id = serializers.CharField()
    criterion_name = serializers.CharField()
    score = serializers.FloatField()
    max_score = serializers.FloatField()
