from rest_framework import serializers
from assessments.domain.value_objects.assessment_type import AssessmentType
from assessments.domain.value_objects.assessment_status import AssessmentStatus
from assessments.presentation.serializers.criterion_serializer import CriterionSerializer

class ResumeAssessmentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    type = serializers.ChoiceField(choices=[AssessmentType.RESUME])
    status = serializers.ChoiceField(choices=AssessmentStatus)
    criteria = CriterionSerializer(read_only=True, many=True)
    created_by = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)