from datetime import datetime
from mongoengine import DateTimeField, DictField, Document, EnumField, FloatField, ReferenceField, StringField
from assessments.domain.value_objects.criterion_type import CriterionType
from assessments.domain.value_objects.assessment_status import AssessmentStatus
from users.models import User

# Create your models here.

class Assessment(Document):
    meta = { 'allow_inheritance': True }

    id = StringField(primary_key=True)
    name = StringField(required=True)
    description = StringField(required=True)
    type = StringField(choices=["RESUME", "CODING", "INTERVIEW"], required=True)
    status = StringField(choices=["DRAFT", "ACTIVE", "CLOSED"], required=True)
    created_by = ReferenceField(User)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

class ResumeAssessment(Assessment):
    pass

class Criterion(Document):
    assessment = ReferenceField(Assessment)
    name = StringField(required=True)
    type = StringField(choices=["KEYWORD_MATCH", "YEARS_EXPERIENCE", "EDUCATION_LEVEL", "SKILLS_MATCH"], required=True)
    weight = FloatField(required=True)
    rules = DictField(required=True)

class AssessmentLink(Document):
    assessment = ReferenceField(Assessment)
    token = StringField(required=True, unique=True)
    expiration = DateTimeField(required=True)
    created_at = DateTimeField(default=datetime.now)