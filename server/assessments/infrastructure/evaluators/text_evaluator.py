from questions.domain.interfaces.answer_evaluator import AnswerEvaluator


class TextEvaluator(AnswerEvaluator):
    """
    Keyword-based evaluator for open-ended (interview) text answers.
    Scores based on how many keywords from the question's keyword list
    appear in the candidate's answer.

    Answers scoring below 30% are flagged for manual review.
    """

    def evaluate(self, candidate_answer: str, question_data: dict) -> dict:
        keywords = [k.lower() for k in question_data.get("keywords", [])]
        answer_lower = candidate_answer.lower()

        if not keywords:
            return {
                "is_correct": None,
                "score": 50.0,
                "feedback": "No keywords defined — flagged for manual review.",
                "needs_review": True,
            }

        matched = sum(1 for kw in keywords if kw in answer_lower)
        score = (matched / len(keywords)) * 100

        needs_review = score < 30
        return {
            "is_correct": score >= 50,
            "score": score,
            "feedback": (
                f"{matched}/{len(keywords)} relevant keywords found."
                + (" Flagged for manual review." if needs_review else "")
            ),
            "needs_review": needs_review,
        }
