
class Criterion():
    def __init__(self, id: int, name: str, type: CriterionType, weight: float, rules: dict) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.weight = weight
        self.rules = rules
        