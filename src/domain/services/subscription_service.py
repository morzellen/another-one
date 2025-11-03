from datetime import datetime
from typing import Optional
from ..entities.subscription import Subscription
from ..enums import PricingPlanEnum, SubscriptionStatusesEnum
from ..value_objects.time_range import TimeRange


class SubscriptionDomainService:
    """
    Domain Service для бизнес-логики, связанной с подписками.
    Следует принципам DDD, вынося сложную бизнес-логику за пределы сущности.
    """

    @staticmethod
    def calculate_subscription_period(
        pricing_plan: PricingPlanEnum, start_time: datetime, duration_days: int | None = None
    ) -> TimeRange:
        """
        Рассчитывает период подписки на основе тарифного плана.

        Args:
            pricing_plan: Тип тарифного плана
            start_time: Время начала подписки
            duration_days: Продолжительность в днях (для LIFETIME и TRIAL используется стандартная)

        Returns:
            TimeRange: Период действия подписки
        """
        if pricing_plan == PricingPlanEnum.LIFETIME:
            return TimeRange(start_time, None)
        elif pricing_plan == PricingPlanEnum.TRIAL:
            from ..constants import TRIAL_PERIOD_IN_DAYS
            import datetime as dt

            end_time = start_time + dt.timedelta(days=TRIAL_PERIOD_IN_DAYS)
            return TimeRange(start_time, end_time)
        else:
            # BASIC или PRO
            if duration_days is None:
                from ..constants import SUB_PERIOD_IN_DAYS

                duration_days = SUB_PERIOD_IN_DAYS
            import datetime as dt

            end_time = start_time + dt.timedelta(days=duration_days)
            return TimeRange(start_time, end_time)

    @staticmethod
    def is_trial_active(subscription: Subscription, current_time: datetime) -> bool:
        """
        Проверяет, является ли подписка пробной и активной на момент времени.
        """
        return (
            subscription.pricing_plan == PricingPlanEnum.TRIAL
            and not SubscriptionDomainService._is_expired_at_time(subscription, current_time)
            and subscription.status == SubscriptionStatusesEnum.ACTIVE
        )

    @staticmethod
    def is_active_at_current_time(subscription: Subscription, current_time: datetime) -> bool:
        """
        Проверяет, активна ли подписка в переданный момент времени.
        """
        if subscription.status != SubscriptionStatusesEnum.ACTIVE:
            return False

        if subscription.pricing_plan == PricingPlanEnum.LIFETIME:
            return True

        return not SubscriptionDomainService._is_expired_at_time(subscription, current_time)

    @staticmethod
    def _is_expired_at_time(subscription: Subscription, current_time: datetime) -> bool:
        """
        Внутренний метод для проверки истечения подписки на определенное время.
        """
        if subscription.period.end_time is None:
            return False
        return current_time > subscription.period.end_time

    @staticmethod
    def can_be_extended_with(subscription: Subscription, new_period: TimeRange) -> bool:
        """
        Проверяет, можно ли продлить подписку новым периодом без пересечений.
        """
        # Lifetime подписки не могут быть продлены
        if subscription.pricing_plan == PricingPlanEnum.LIFETIME:
            return False

        # Проверяем пересечение с новым периодом
        current_end = subscription.period.end_time
        if current_end is None:
            return True  # lifetime не имеет конца (хотя выше проверка на LIFETIME)
        return current_end <= new_period.start_time

    @staticmethod
    def calculate_expiration_date(
        subscription: Subscription, current_time: datetime
    ) -> Optional[datetime]:
        """
        Рассчитывает дату истечения подписки.
        """
        if subscription.pricing_plan == PricingPlanEnum.LIFETIME:
            return None
        return subscription.period.end_time

    @staticmethod
    def should_be_active(subscription: Subscription, current_time: datetime) -> bool:
        """
        Определяет, должна ли подписка быть активной в данный момент времени.
        Учитывает статус, тип подписки и срок действия.
        """
        if subscription.status != SubscriptionStatusesEnum.ACTIVE:
            return False

        if subscription.pricing_plan == PricingPlanEnum.LIFETIME:
            return True

        return not SubscriptionDomainService._is_expired_at_time(subscription, current_time)

    @staticmethod
    def calculate_next_renewal_date(
        subscription: Subscription, renewal_period_days: int = 30
    ) -> Optional[datetime]:
        """
        Рассчитывает дату следующего продления подписки.
        """
        if subscription.pricing_plan == PricingPlanEnum.LIFETIME:
            return None

        import datetime as dt

        if subscription.period.end_time is None:
            return None

        return subscription.period.end_time + dt.timedelta(days=renewal_period_days)
