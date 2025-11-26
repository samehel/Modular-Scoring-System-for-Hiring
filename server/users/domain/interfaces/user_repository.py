from abc import ABC, abstractmethod
from users.domain.entities.user import User

class UserRepository(ABC):
    
    @abstractmethod
    def save(self, user: User) -> User | None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def find_by_id(self, Id: str) -> User | None:
        pass

    @abstractmethod
    def update(self, user: User) -> User | None:
        pass

    @abstractmethod
    def delete(self, Id: str) -> bool:
        pass
