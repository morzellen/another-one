import uuid
from datetime import datetime
from uuid import UUID
from ..enums import AuthProviderEnum


class AuthIdentity:
    """
    Entity. Represents authentication method for a user.
    Unique by (user_id, provider).
    """

    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        provider_user_id: str,
        provider: AuthProviderEnum,
        created_at: datetime,
    ):
        self._id = id
        self._user_id = user_id
        self._provider_user_id = provider_user_id
        self._provider = provider
        self._created_at = created_at

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def provider_user_id(self) -> str:
        return self._provider_user_id

    @property
    def provider(self) -> AuthProviderEnum:
        return self._provider

    @property
    def created_at(self) -> datetime:
        return self._created_at

    # Удаляем фабричные методы из сущности
    def is_native_provider(self) -> bool:
        """Check if this identity uses native authentication provider."""
        return self.provider == AuthProviderEnum.NATIVE
