from rest_framework import serializers
from assessments.presentation.serializers.resume_data_serializer import ResumeDataSerializer
from assessments.presentation.serializers.score_breakdown_serializer import ScoreBreakdownSerializer


class AssessmentResultSerializer(serializers.Serializer):
    """Full assessment result with parsed resume data and score breakdown."""
    id = serializers.CharField(read_only=True)
    assessment_id = serializers.CharField(read_only=True)
    assessment_name = serializers.CharField(read_only=True, required=False)
    assessment_type = serializers.CharField(read_only=True, required=False)
    total_score = serializers.FloatField(read_only=True)
    submitted_at = serializers.CharField(read_only=True)
    parsed_data = ResumeDataSerializer(read_only=True, required=False)
    score_breakdown = ScoreBreakdownSerializer(many=True, read_only=True, required=False)
    candidate_id = serializers.CharField(read_only=True, required=False, allow_null=True)
