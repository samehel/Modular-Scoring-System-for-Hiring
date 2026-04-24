from abc import ABC, abstractmethod
from typing import List
from questions.domain.entities.question_entities import QuestionBase


class QuestionGenerator(ABC):

    @abstractmethod
    def generate(self, topic: str, difficulty: str, count: int) -> List[QuestionBase]:
        """Generate `count` questions for the given topic and difficulty."""
        pass
