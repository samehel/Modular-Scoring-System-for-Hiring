
from abc import ABC, abstractmethod


class ResumeParser(ABC):

    @abstractmethod
    def parse(self, file: bytes) -> dict:
        pass