from dataclasses import dataclass, field
from typing import List

from assessments.domain.entities.assessment_base import AssessmentBase
from questions.domain.entities.question_entities import QuestionBase


@dataclass
class CodingAssessment(AssessmentBase):
    """Domain entity for a coding/MCQ assessment."""
    topics: List[str] = field(default_factory=list)
    difficulty: str = "MEDIUM"
    question_count: int = 5
    time_limit: int = 60  # minutes
    questions: List[QuestionBase] = field(default_factory=list)
