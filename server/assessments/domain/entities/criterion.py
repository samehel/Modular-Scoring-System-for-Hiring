
from typing import Optional
from assessments.domain.value_objects.criterion_type import CriterionType

class Criterion():
    def __init__(self, id: Optional[int], name: str, type: CriterionType, weight: float, rules: dict) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.weight = weight
        self.rules = rules
        