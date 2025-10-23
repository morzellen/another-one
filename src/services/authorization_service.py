from uuid import UUID
from ..entities.user_studio_membership import UserStudioMembership
from ..repositories.user_studio_membership_repository import (
    UserStudioMembershipRepository,
)
from ..constants import ROLE_FUNCTIONALITY


class AuthorizationService:
    def __init__(self, membership_repo: UserStudioMembershipRepository):
        self.membership_repo = membership_repo

    def can_access_studio(self, user_id: UUID, studio_id: UUID) -> bool:
        """Проверяет, может ли пользователь получить доступ к студии."""
        membership = self.membership_repo.find_by_user_and_studio(user_id, studio_id)
        return membership is not None and membership.is_active()

    def get_user_functionality_in_studio(
        self, user_id: UUID, studio_id: UUID
    ) -> list[str]:
        """Возвращает список функций, доступных пользователю в студии."""
        membership = self.membership_repo.find_by_user_and_studio(user_id, studio_id)
        if not membership:
            return []

        functionality = []
        for role in membership.roles:
            functionality.extend(ROLE_FUNCTIONALITY.get(role, []))
        return functionality
