from typing import List


class CreateInterviewAssessmentDTO:
    def __init__(
        self,
        name: str,
        description: str,
        categories: List[str],
        time_limit: int,
        question_count: int,
    ) -> None:
        self.name = name
        self.description = description
        self.categories = categories
        self.time_limit = time_limit
        self.question_count = question_count
