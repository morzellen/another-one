from datetime import datetime
from typing import List
from uuid import UUID

from ..enums import AuthProviderEnum, UserRoleEnum, UserStatusesEnum

from ..entities.user import User
from ..entities.auth_identity import AuthIdentity
from ..entities.user_studio_membership import UserStudioMembership
from ..repositories.user_repository import UserRepository
from ..repositories.auth_identity_repository import AuthIdentityRepository
from ..repositories.user_studio_membership_repository import (
    UserStudioMembershipRepository,
)
from ..errors import AuthenticationError, UserNotFoundError, RoleAssignmentError
from ..value_objects.value_objects import ContactInfo, Email, PersonalInfo


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        auth_identity_repo: AuthIdentityRepository,
        membership_repo: UserStudioMembershipRepository,
    ):
        self.user_repo = user_repo
        self.auth_identity_repo = auth_identity_repo
        self.membership_repo = membership_repo

    def register_user(self, email: str, password: str) -> User:
        """Регистрирует нового пользователя."""
        user = User(
            id=UUID(...),
            contact_info=ContactInfo(email=Email(email)),
            created_at=datetime.now(),
        )
        self.user_repo.save(user)

        auth_identity = AuthIdentity.create_native(
            user_id=user.id,
            password_hash=PasswordHasher().hash(password),
            now=datetime.now(),
        )
        self.auth_identity_repo.save(auth_identity)

        return user

    def assign_role_to_studio(
        self, user_id: UUID, studio_id: UUID, role: UserRoleEnum
    ) -> UserStudioMembership:
        """Назначает роль пользователю в студии."""
        membership = self.membership_repo.find_by_user_and_studio(user_id, studio_id)
        if not membership:
            membership = UserStudioMembership(
                user_id=user_id,
                studio_id=studio_id,
                roles={role},
                joined_at=datetime.now(),
                status=UserStatusesEnum.ACTIVE,
            )
        else:
            if membership.status == UserStatusesEnum.BANNED:
                raise RoleAssignmentError("Cannot assign role to banned user")
            membership.add_role(role)

        self.membership_repo.save(membership)
        return membership

    def get_user_roles_in_studio(
        self, user_id: UUID, studio_id: UUID
    ) -> List[UserRoleEnum]:
        """Возвращает роли пользователя в студии."""
        membership = self.membership_repo.find_by_user_and_studio(user_id, studio_id)
        if not membership:
            return []
        return list(membership.roles)

    def get_user_functionality_in_studio(
        self, user_id: UUID, studio_id: UUID
    ) -> List[str]:
        """Возвращает функциональность пользователя в студии."""
        membership = self.membership_repo.find_by_user_and_studio(user_id, studio_id)
        if not membership:
            return []
        return membership.get_functionality()

    def update_user_contact_info(self, user_id: UUID, new_contact_info: ContactInfo):
        """Обновляет контактную информацию пользователя."""
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")

        # Проверяем, не занят ли новый email
        if new_contact_info.email and new_contact_info.email != user.contact_info.email:
            existing_user = self.user_repo.find_by_email(new_contact_info.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email is already in use")

        user.contact_info = new_contact_info
        user.updated_at = datetime.now()
        self.user_repo.save(user)

    def update_user_personal_info(self, user_id: UUID, new_personal_info: PersonalInfo):
        """Обновляет персональную информацию пользователя."""
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")

        user.personal_info = new_personal_info
        user.has_custom_profile = True
        user.updated_at = datetime.now()
        self.user_repo.save(user)
