from typing import List


class CreateCodingAssessmentDTO:
    def __init__(
        self,
        name: str,
        description: str,
        topics: List[str],
        difficulty: str,
        question_count: int,
        time_limit: int,
    ) -> None:
        self.name = name
        self.description = description
        self.topics = topics
        self.difficulty = difficulty
        self.question_count = question_count
        self.time_limit = time_limit
