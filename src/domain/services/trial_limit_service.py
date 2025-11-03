from datetime import datetime
from uuid import UUID
from typing import List
from ..entities.user_studio_membership import UserStudioMembership
from ..entities.subscription import Subscription
from ..enums import UserRoleEnum, PricingPlanEnum
from ..errors import TrialLimitExceededError
from ..constants import MAX_TRIALS_PER_OWNER


class TrialLimitService:
    """
    Domain Service для управления ограничениями на пробные периоды.
    Следует принципам DDD, вынося бизнес-логику проверки ограничений за пределы сущностей.
    """

    @staticmethod
    def can_activate_trial_for_owner(existing_subscriptions: List[Subscription]) -> bool:
        """
        Проверяет, может ли владелец активировать пробную подписку.

        Args:
            existing_subscriptions: Список существующих подписок для студии

        Returns:
            bool: True, если можно активировать пробную подписку
        """

        # Подсчитываем количество пробных подписок для этой студии
        trial_count = sum(
            1 for sub in existing_subscriptions if sub.pricing_plan == PricingPlanEnum.TRIAL
        )

        return trial_count < MAX_TRIALS_PER_OWNER

    @staticmethod
    def validate_trial_activation(
        owner_membership: UserStudioMembership, existing_subscriptions: List[Subscription]
    ) -> None:
        """
        Валидирует возможность активации пробной подписки.
        Выбрасывает исключение, если пробная подписка не может быть активирована.

        Args:
            owner_membership: Членство владельца в студии
            existing_subscriptions: Список существующих подписок для студии

        Raises:
            TrialLimitExceededError: Если лимит пробных периодов превышен
        """
        if not TrialLimitService.can_activate_trial_for_owner(
            owner_membership, existing_subscriptions
        ):
            raise TrialLimitExceededError(
                f"Owner has already used the maximum number of trial subscriptions ({MAX_TRIALS_PER_OWNER})"
            )
