from questions.domain.interfaces.answer_evaluator import AnswerEvaluator
from assessments.infrastructure.evaluators.mcq_evaluator import MCQEvaluator
from assessments.infrastructure.evaluators.coding_evaluator import CodingEvaluator
from assessments.infrastructure.evaluators.text_evaluator import TextEvaluator


class AnswerEvaluatorFactory:
    """Returns the appropriate evaluator for a given question type (Factory pattern)."""

    _evaluators = {
        "MCQ": MCQEvaluator,
        "CODING": CodingEvaluator,
        "TEXT": TextEvaluator,
    }

    @classmethod
    def get_evaluator(cls, question_type: str) -> AnswerEvaluator:
        evaluator_class = cls._evaluators.get(question_type.upper())
        if evaluator_class is None:
            raise ValueError(f"No evaluator registered for question type: {question_type}")
        return evaluator_class()
