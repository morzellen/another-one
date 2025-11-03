from datetime import datetime
from typing import List
from ..entities.studio import Studio
from ..entities.subscription import Subscription
from ..entities.user_studio_membership import UserStudioMembership
from ..enums import UserRoleEnum, PricingPlanEnum


class StudioDomainService:
    """
    Domain Service для бизнес-логики, связанной со студиями.
    Следует принципам DDD, вынося сложную бизнес-логику за пределы сущности.
    """

    @staticmethod
    def can_create_studio_with_trial(
        owner_membership: UserStudioMembership, existing_subscriptions: List[Subscription]
    ) -> bool:
        """
        Проверяет, может ли владелец создать студию с пробной подпиской.
        """
        if not owner_membership.has_role(UserRoleEnum.OWNER):
            return False

        # Проверяем лимит пробных периодов
        from .trial_limit_service import TrialLimitService

        return TrialLimitService.can_activate_trial_for_owner(existing_subscriptions)

    @staticmethod
    def can_assign_subscription(
        studio: Studio, new_subscription: Subscription, current_subscription: Subscription | None
    ) -> bool:
        """
        Проверяет, можно ли назначить новую подписку студии.
        """
        # Для пробных подписок - только если нет текущей подписки
        if new_subscription.pricing_plan == PricingPlanEnum.TRIAL:
            return current_subscription is None

        # Для других типов подписок - можно заменить текущую
        return True

    @staticmethod
    def should_activate_trial_automatically(
        studio: Studio, trial_subscription: Subscription
    ) -> bool:
        """
        Определяет, должна ли пробная подписка быть активирована автоматически.
        Пробные подписки считаются активными по умолчанию.
        """
        return (
            trial_subscription.pricing_plan == PricingPlanEnum.TRIAL
            and trial_subscription.status.name != "ACTIVE"  # Не активна в данный момент
        )

    @staticmethod
    def calculate_studio_expiration_date(
        studio: Studio, current_subscription: Subscription | None, current_time: datetime
    ) -> datetime | None:
        """
        Рассчитывает дату истечения подписки студии.
        """
        if current_subscription is None:
            return None

        from .subscription_service import SubscriptionDomainService

        return SubscriptionDomainService.calculate_expiration_date(
            current_subscription, current_time
        )

    @staticmethod
    def is_studio_subscription_active(
        studio: Studio, current_subscription: Subscription | None, current_time: datetime
    ) -> bool:
        """
        Проверяет, активна ли подписка студии.
        """
        if current_subscription is None:
            return False

        from .subscription_service import SubscriptionDomainService

        return SubscriptionDomainService.is_active_at_current_time(
            current_subscription, current_time
        )
