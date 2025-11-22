import re

class Email():
    email: str

    def __init__(self, email: str):
        self.email = email

    def validate(self) -> bool:
        return re.match(r"^[^@]+@[^@]+\.[^@]+", self.email) is not None