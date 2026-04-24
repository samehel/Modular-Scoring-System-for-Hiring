from abc import ABC, abstractmethod
from typing import List, Optional
from questions.domain.entities.question_entities import QuestionBase


class QuestionRepository(ABC):

    @abstractmethod
    def save(self, question: QuestionBase) -> QuestionBase:
        pass

    @abstractmethod
    def get_by_id(self, question_id: str) -> Optional[QuestionBase]:
        pass

    @abstractmethod
    def get_by_topic(self, topic: str, question_type: str) -> List[QuestionBase]:
        pass

    @abstractmethod
    def get_random(self, topic: str, difficulty: str, count: int, question_type: str) -> List[QuestionBase]:
        pass
