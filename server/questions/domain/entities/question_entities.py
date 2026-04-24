from dataclasses import dataclass, field
from typing import List


@dataclass
class QuestionBase:
    id: str
    title: str
    description: str
    difficulty: str      # DifficultyLevel.value
    topic: str
    question_type: str   # QuestionType.value


@dataclass
class MCQQuestionEntity(QuestionBase):
    choices: List[str] = field(default_factory=list)
    correct_answer: str = ""


@dataclass
class CodingQuestionEntity(QuestionBase):
    problem_statement: str = ""
    test_cases: List[dict] = field(default_factory=list)
    solution_code: str = ""


@dataclass
class TextQuestionEntity(QuestionBase):
    category: str = "BEHAVIORAL"   # QuestionCategory.value
    keywords: List[str] = field(default_factory=list)
