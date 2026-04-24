from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    FloatField,
    ListField,
    DictField,
    BooleanField,
    DateTimeField,
)


class Question(Document):
    """Base question document — abstract via allow_inheritance."""
    meta = {'allow_inheritance': True}

    title = StringField(required=True)
    description = StringField(required=True)
    difficulty = StringField(choices=['EASY', 'MEDIUM', 'HARD'], required=True)
    topic = StringField(required=True)
    question_type = StringField(choices=['MCQ', 'CODING', 'TEXT'], required=True)
    created_at = DateTimeField(default=datetime.now)


class MCQQuestion(Question):
    """Multiple-choice question with a list of choices and a correct answer."""
    choices = ListField(StringField(), required=True)   # e.g. ['O(n)', 'O(log n)', ...]
    correct_answer = StringField(required=True)         # must match one of choices


class CodingQuestion(Question):
    """Coding problem with test cases (input/expected_output pairs)."""
    problem_statement = StringField(required=True)
    test_cases = ListField(DictField())   # [{input: ..., expected_output: ...}]
    solution_code = StringField(default='')


class TextQuestion(Question):
    """Open-ended question (used for interviews)."""
    category = StringField(
        choices=['BEHAVIORAL', 'TECHNICAL', 'EXPERIENCE', 'EDUCATION'],
        required=True,
    )
    keywords = ListField(StringField())   # keywords used for keyword-based scoring
