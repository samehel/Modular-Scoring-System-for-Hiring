from abc import ABC, abstractmethod


class AnswerEvaluator(ABC):

    @abstractmethod
    def evaluate(self, candidate_answer: str, question_data: dict) -> dict:
        """
        Evaluate a candidate's answer against the question.

        Returns:
            { is_correct: bool, score: float (0–100), feedback: str }
        """
        pass
