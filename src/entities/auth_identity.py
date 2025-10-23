from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ..enums import AuthProviderEnum


@dataclass
class AuthIdentity:
    """
    Entity. Represents authentication method for a user.
    Unique by (user_id, provider).
    """

    id: UUID  # Генерируемый ID для репозитория
    user_id: UUID
    provider_user_id: str  # maybe should be UUID?
    provider: AuthProviderEnum
    created_at: datetime

    @classmethod
    def create_native(
        cls, user_id: UUID, password_hash: str, now: datetime
    ) -> "AuthIdentity":
        return cls(
            id=UUID(...),
            user_id=user_id,
            provider=AuthProviderEnum.NATIVE,
            provider_user_id=password_hash,
            created_at=now,
        )

    @classmethod
    def create_oauth2(
        cls, user_id: UUID, provider: str, provider_user_id: str, now: datetime
    ) -> "AuthIdentity":
        return cls(
            id=UUID(...),
            user_id=user_id,
            provider=AuthProviderEnum(provider),
            provider_user_id=provider_user_id,
            created_at=now,
        )
