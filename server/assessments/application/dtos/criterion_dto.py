from assessments.domain.value_objects.criterion_type import CriterionType

class CriterionDTO():

    def __init__(self, name: str, type: CriterionType, weight: float, rules: dict) -> None:
        self.name = name
        self.type = type
        self.weight = weight
        self.rules = rules