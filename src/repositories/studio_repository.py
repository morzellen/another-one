from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from ..entities.studio import Studio


class StudioRepository(ABC):
    @abstractmethod
    def find_by_id(self, studio_id: UUID) -> Optional[Studio]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Studio]:
        pass

    @abstractmethod
    def save(self, studio: Studio):
        pass

    @abstractmethod
    def count_trials_by_owner(self, owner_id: UUID) -> int:
        pass


class InMemoryStudioRepository(StudioRepository):
    def __init__(self):
        self.studios = {}  # UUID -> Studio
        self.trial_counts = {}  # owner_id -> count

    def find_by_id(self, studio_id: UUID) -> Optional[Studio]:
        return self.studios.get(studio_id)

    def find_by_name(self, name: str) -> Optional[Studio]:
        for studio in self.studios.values():
            if studio.name == name:
                return studio
        return None

    def save(self, studio: Studio):
        self.studios[studio.id] = studio
        # Отслеживаем пробники для TrialLimitService
        if studio.is_on_trial:
            owner_id = studio.owner_id
            self.trial_counts[owner_id] = self.trial_counts.get(owner_id, 0) + 1

    def count_trials_by_owner(self, owner_id: UUID) -> int:
        return self.trial_counts.get(owner_id, 0)
