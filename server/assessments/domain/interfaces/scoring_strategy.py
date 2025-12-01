
from abc import ABC, abstractmethod
from assessments.domain.entities.criterion import Criterion

class ScoringStrategy(ABC):

    @abstractmethod
    def score(self, data: dict, criteria: list[Criterion]) -> float:
        pass