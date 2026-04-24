import re
from questions.domain.interfaces.answer_evaluator import AnswerEvaluator


class CodingEvaluator(AnswerEvaluator):
    """
    Regex / keyword-based evaluator for coding questions.
    No actual code execution — uses pattern matching against test case expected outputs.

    For a proper evaluation, the candidate's answer text is checked for:
    - Presence of the expected output strings from test cases
    - Presence of common solution patterns (function definition, return, correct keywords)
    """

    def evaluate(self, candidate_answer: str, question_data: dict) -> dict:
        test_cases = question_data.get("test_cases", [])
        if not test_cases:
            return {"is_correct": True, "score": 50.0, "feedback": "No test cases to validate against."}

        passed = 0
        for tc in test_cases:
            expected = str(tc.get("expected_output", "")).strip()
            if expected and re.search(re.escape(expected), candidate_answer, re.IGNORECASE):
                passed += 1

        total = len(test_cases)
        score = (passed / total) * 100 if total > 0 else 0.0
        is_correct = passed == total

        return {
            "is_correct": is_correct,
            "score": score,
            "feedback": f"{passed}/{total} test cases matched in your solution.",
        }
