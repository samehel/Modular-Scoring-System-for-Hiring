
from datetime import datetime

class LinkToken():
    def __init__(self, value: str, expiration: datetime) -> None:
        self.value = value
        self.expiration = expiration