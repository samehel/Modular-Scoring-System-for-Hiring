from questions.domain.interfaces.answer_evaluator import AnswerEvaluator


class MCQEvaluator(AnswerEvaluator):
    """
    Binary evaluator for multiple-choice questions.
    Compares the candidate's answer (case-insensitive) with the correct answer.
    """

    def evaluate(self, candidate_answer: str, question_data: dict) -> dict:
        correct = str(question_data.get("correct_answer", "")).strip().lower()
        given = str(candidate_answer).strip().lower()
        is_correct = given == correct
        return {
            "is_correct": is_correct,
            "score": 100.0 if is_correct else 0.0,
            "feedback": "Correct!" if is_correct else f"Incorrect. The correct answer is: {question_data.get('correct_answer')}",
        }
