import re

class Email():
    def __init__(self, email: str):
        self.value = email

    def validate(self) -> bool:
        return re.match(r"^[^@]+@[^@]+\.[^@]+", self.value) is not None