from uuid import UUID
from ..repositories.studio_repository import StudioRepository
from ..constants import MAX_TRIALS_PER_OWNER


class TrialLimitService:
    def __init__(self, studio_repo: StudioRepository):
        self.studio_repo = studio_repo

    def can_activate_trial_for_owner(self, owner_id: UUID) -> bool:
        """Проверяет, может ли владелец активировать пробный период."""
        # Реализация: запрос к базе данных, сколько пробников уже было
        count = self.studio_repo.count_trials_by_owner(owner_id)
        return count < MAX_TRIALS_PER_OWNER  # Например, один пробник на владельца
