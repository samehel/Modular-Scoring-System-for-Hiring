from datetime import datetime
from mongoengine import DateTimeField, DictField, Document, EnumField, FloatField, ReferenceField, StringField
from assessments.domain.value_objects.assessment_type import AssessmentType
from assessments.domain.value_objects.criterion_type import CriterionType
from assessments.domain.value_objects.assessment_status import AssessmentStatus
from users.models import User

# Create your models here.

class Assessment(Document):
    id = StringField(primary_key=True)
    name = StringField(required=True)
    description = StringField(required=True)
    type = EnumField(AssessmentType)
    status = EnumField(AssessmentStatus)
    created_by = ReferenceField(User)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

class ResumeAssessment(Assessment):
    pass

class Criterion(Document):
    assessment = ReferenceField(Assessment)
    name = StringField(required=True)
    type = EnumField(CriterionType)
    weight = FloatField(required=True)
    rules = DictField(required=True)

class AssessmentLink(Document):
    assessment = ReferenceField(Assessment)
    token = StringField(required=True, unique=True)
    expiration = DateTimeField(required=True)
    created_at = DateTimeField(default=datetime.now)