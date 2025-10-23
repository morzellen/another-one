# src/services/authentication_service.py
from datetime import datetime
from uuid import UUID
from ..entities.user import User
from ..entities.auth_identity import AuthIdentity
from ..repositories.user_repository import UserRepository
from ..repositories.auth_identity_repository import AuthIdentityRepository
from ..errors import AuthenticationError
from ..value_objects.value_objects import Email, PasswordHasher


class AuthenticationService:
    def __init__(
        self,
        user_repo: UserRepository,
        auth_identity_repo: AuthIdentityRepository,
    ):
        self.user_repo = user_repo
        self.auth_identity_repo = auth_identity_repo

    def authenticate_native(self, login: str, password: str) -> User:
        """Аутентифицирует пользователя по логину/паролю."""
        email = Email(login)
        user = self.user_repo.find_by_email(email)
        if not user:
            raise AuthenticationError("User not found")

        auth_identity = self.auth_identity_repo.find_by_user_and_provider(
            user.id, AuthProviderEnum.NATIVE
        )
        if not auth_identity:
            raise AuthenticationError("No native authentication method")

        if not auth_identity.verify_password(password, PasswordHasher()):
            raise AuthenticationError("Invalid password")

        return user

    def authenticate_oauth2(self, provider: str, token: str) -> User:
        """Аутентифицирует через OAuth2."""
        # Логика получения user_id по token и provider
        # Пример: вызов API провайдера, получение profile_id
        profile_id = self._get_profile_id_from_token(provider, token)
        user = self.user_repo.find_by_provider_id(provider, profile_id)
        if not user:
            # Создаём нового пользователя
            user = User(id=UUID(...), contact_info=ContactInfo(email=None))
            self.user_repo.save(user)
            auth_identity = AuthIdentity.create_oauth2(
                user_id=user.id,
                provider=provider,
                provider_user_id=profile_id,
                now=datetime.now(),
            )
            self.auth_identity_repo.save(auth_identity)
        else:
            # Проверяем, есть ли уже запись в AuthIdentity
            existing = self.auth_identity_repo.find_by_user_and_provider(
                user.id, provider
            )
            if not existing:
                auth_identity = AuthIdentity.create_oauth2(
                    user_id=user.id,
                    provider=provider,
                    provider_user_id=profile_id,
                    now=datetime.now(),
                )
                self.auth_identity_repo.save(auth_identity)

        return user

    def _get_profile_id_from_token(self, provider: str, token: str) -> str:
        # Реализация зависит от провайдера
        # Можно вынести в отдельный OAuth2ClientService
        pass
