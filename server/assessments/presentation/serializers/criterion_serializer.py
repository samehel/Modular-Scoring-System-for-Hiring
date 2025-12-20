from rest_framework import serializers
from assessments.domain.value_objects.criterion_type import CriterionType

class CriterionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=[ct.value for ct in CriterionType])
    weight = serializers.FloatField()
    rules = serializers.DictField()