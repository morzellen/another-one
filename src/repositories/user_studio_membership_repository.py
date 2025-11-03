from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..entities.user_studio_membership import UserStudioMembership


class UserStudioMembershipRepository(ABC):
    @abstractmethod
    def find_by_user_and_studio(
        self, user_id: UUID, studio_id: UUID
    ) -> Optional[UserStudioMembership]:
        pass

    @abstractmethod
    def find_by_user(self, user_id: UUID) -> List[UserStudioMembership]:
        pass

    @abstractmethod
    def save(self, membership: UserStudioMembership):
        pass


class InMemoryUserStudioMembershipRepository(UserStudioMembershipRepository):
    def __init__(self):
        self.memberships = {}  # (user_id, studio_id) -> membership
        self.by_user = {}  # user_id -> list of memberships

    def find_by_user_and_studio(
        self, user_id: UUID, studio_id: UUID
    ) -> Optional[UserStudioMembership]:
        return self.memberships.get((user_id, studio_id))

    def find_by_user(self, user_id: UUID) -> List[UserStudioMembership]:
        return self.by_user.get(user_id, [])

    def save(self, membership: UserStudioMembership):
        key = (membership.user_id, membership.studio_id)
        self.memberships[key] = membership

        # Обновляем индекс по пользователю
        if membership.user_id not in self.by_user:
            self.by_user[membership.user_id] = []
        # Удаляем старую запись, если есть
        self.by_user[membership.user_id] = [
            m
            for m in self.by_user[membership.user_id]
            if m.studio_id != membership.studio_id
        ]
        self.by_user[membership.user_id].append(membership)
