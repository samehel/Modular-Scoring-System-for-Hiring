from rest_framework import serializers
from assessments.domain.value_objects.criterion_type import CriterionType

class CriterionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=CriterionType)
    weight = serializers.FloatField()
    rules = serializers.DictField()