from dataclasses import dataclass, field
from typing import List

from assessments.domain.entities.assessment_base import AssessmentBase
from questions.domain.entities.question_entities import TextQuestionEntity


@dataclass
class InterviewAssessment(AssessmentBase):
    """Domain entity for an interview (text-question) assessment."""
    categories: List[str] = field(default_factory=list)   # QuestionCategory values
    time_limit: int = 45  # minutes
    question_count: int = 5
    questions: List[TextQuestionEntity] = field(default_factory=list)
