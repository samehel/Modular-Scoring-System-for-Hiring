
from abc import ABC, abstractmethod

from assessments.domain.entities.assessment_base import AssessmentBase
from assessments.domain.value_objects.link_token import LinkToken

class AssessmentRepository(ABC):

    @abstractmethod
    def save(self, assessment: AssessmentBase) -> AssessmentBase | None:
        pass

    @abstractmethod
    def save_link(self, assessment_id: str, token: LinkToken) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> AssessmentBase | None:
        pass

    @abstractmethod
    def find_by_link_token(self, linkToken: str) -> AssessmentBase | None:
        pass

    @abstractmethod
    def find_by_creator(self, creator: str) -> list[AssessmentBase] | None:
        pass

    @abstractmethod
    def update(self, assessment: AssessmentBase) -> AssessmentBase | None:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass