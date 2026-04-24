from abc import ABC, abstractmethod
from typing import List, Optional


class ResultRepository(ABC):

    @abstractmethod
    def save_result(self, result_data: dict) -> dict:
        pass

    @abstractmethod
    def get_result_by_id(self, result_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_results_for_assessment(self, assessment_id: str) -> List[dict]:
        pass

    @abstractmethod
    def get_results_for_candidate(self, candidate_id: str) -> List[dict]:
        pass
