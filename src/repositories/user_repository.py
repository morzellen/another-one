from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.user import User
from ..value_objects.value_objects import Email


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def find_by_email(self, email: Email) -> User | None:
        pass

    @abstractmethod
    def find_by_provider_id(self, provider: str, provider_user_id: str) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User):
        pass
