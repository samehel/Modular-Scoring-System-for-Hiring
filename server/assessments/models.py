from datetime import datetime
from mongoengine import (
    DateTimeField, DictField, Document, FloatField,
    ReferenceField, StringField, ListField, IntField, BooleanField,
)
from users.models import User

# ── Core Assessment Documents ────────────────────────────────────────────────

class Assessment(Document):
    meta = {'allow_inheritance': True}

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


class CodingAssessment(Assessment):
    topics = ListField(StringField())
    difficulty = StringField(choices=["EASY", "MEDIUM", "HARD"], default="MEDIUM")
    question_count = IntField(default=5)
    time_limit = IntField(default=60)     # minutes
    # Embedded question IDs (from the questions app)
    question_ids = ListField(StringField())


class InterviewAssessment(Assessment):
    categories = ListField(StringField())
    time_limit = IntField(default=45)     # minutes
    question_count = IntField(default=5)
    question_ids = ListField(StringField())


# ── Criterion ────────────────────────────────────────────────────────────────

class Criterion(Document):
    assessment = ReferenceField(Assessment)
    name = StringField(required=True)
    type = StringField(
        choices=["KEYWORD_MATCH", "YEARS_EXPERIENCE", "EDUCATION_LEVEL", "SKILLS_MATCH"],
        required=True,
    )
    weight = FloatField(required=True)
    rules = DictField(required=True)


# ── Assessment Link ───────────────────────────────────────────────────────────

class AssessmentLink(Document):
    assessment = ReferenceField(Assessment)
    token = StringField(required=True, unique=True)
    expiration = DateTimeField(required=True)
    created_at = DateTimeField(default=datetime.now)


# ── Results ──────────────────────────────────────────────────────────────────

class AssessmentResult(Document):
    assessment = ReferenceField(Assessment)
    candidate = ReferenceField(User, null=True)
    total_score = FloatField(required=True)
    submitted_at = DateTimeField(required=True)


class ResumeData(Document):
    assessment_result = ReferenceField(AssessmentResult, unique=True)
    parsed_data = DictField(required=True)


class ScoreBreakdown(Document):
    result = ReferenceField(AssessmentResult)
    criterion = ReferenceField(Criterion)
    score = FloatField(required=True)


# ── Test Sessions (Phase 9) ───────────────────────────────────────────────────

class TestSession(Document):
    assessment = ReferenceField(Assessment, required=True)
    candidate = ReferenceField(User, null=True)
    start_time = DateTimeField(default=datetime.now)
    end_time = DateTimeField(null=True)
    status = StringField(choices=["IN_PROGRESS", "COMPLETED", "EXPIRED"], default="IN_PROGRESS")


class CandidateAnswer(Document):
    session = ReferenceField(TestSession, required=True)
    question_id = StringField(required=True)   # ID from questions app
    question_type = StringField(choices=["MCQ", "CODING", "TEXT"], required=True)
    answer_text = StringField(default="")
    is_correct = BooleanField(null=True)
    score = FloatField(default=0.0)
