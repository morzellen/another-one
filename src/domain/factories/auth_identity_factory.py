import uuid
from datetime import datetime
from typing import Union
from uuid import UUID

from ..entities.auth_identity import AuthIdentity
from ..enums import AuthProviderEnum


class AuthIdentityFactory:
    """
    Domain Service Factory для создания AuthIdentity.
    Следует принципам DDD, вынося создание сущности за пределы самой сущности.
    """

    @staticmethod
    def create_native(user_id: UUID, password: str, created_at: datetime) -> AuthIdentity:
        """
        Создает AuthIdentity для нативной аутентификации.
        В реальной системе здесь может быть хеширование пароля.
        """
        # В реальной системе нужно хешировать пароль
        # password_hash = hash_password(password)
        return AuthIdentity(
            id=uuid.uuid4(),
            user_id=user_id,
            provider_user_id=password,  # В реальности это будет хеш
            provider=AuthProviderEnum.NATIVE,
            created_at=created_at,
        )

    @staticmethod
    def create_oauth2(
        user_id: UUID,
        provider: Union[AuthProviderEnum, str],
        provider_user_id: str,
        created_at: datetime,
    ) -> AuthIdentity:
        """
        Создает AuthIdentity для OAuth2 аутентификации.
        """
        if isinstance(provider, str):
            provider = AuthProviderEnum(provider)

        return AuthIdentity(
            id=uuid.uuid4(),
            user_id=user_id,
            provider_user_id=provider_user_id,
            provider=provider,
            created_at=created_at,
        )
