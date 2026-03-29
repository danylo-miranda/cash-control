from abc import ABC, abstractmethod
from cash_control.domain.entities.user import User

class UserRepository(ABC):
    
    @abstractmethod
    def create(self, user: User) -> User:
        pass