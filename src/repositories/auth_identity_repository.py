from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from ..entities.auth_identity import AuthIdentity
from ..domain.enums import AuthProviderEnum


class AuthIdentityRepository(ABC):
    @abstractmethod
    def find_by_user_and_provider(
        self, user_id: UUID, provider: AuthProviderEnum
    ) -> Optional[AuthIdentity]:
        pass

    @abstractmethod
    def save(self, identity: AuthIdentity):
        pass


class InMemoryAuthIdentityRepository(AuthIdentityRepository):
    def __init__(self):
        self.identities = {}  # key: (user_id, provider)

    def find_by_user_and_provider(
        self, user_id: UUID, provider: AuthProviderEnum
    ) -> Optional[AuthIdentity]:
        return self.identities.get((user_id, provider))

    def save(self, identity: AuthIdentity):
        self.identities[(identity.user_id, identity.provider)] = identity
