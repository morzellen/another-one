from datetime import datetime
from uuid import UUID
from ..value_objects.subscription_period import SubscriptionPeriod
from ..enums import PricingPlanEnum, SubscriptionStatusesEnum


class Subscription:
    """
    Это план подписки для студии.
    Привязывается к студии при создании, включая пробные периоды (без необходимости оплаты).
    Пробные периоды рассматриваются как активные подписки с фиксированным сроком и без payment_id.
    """

    def __init__(
        self,
        id: UUID,
        studio_id: UUID,
        pricing_plan: PricingPlanEnum,
        period: SubscriptionPeriod,
        created_at: datetime,
        updated_at: datetime,
        payment_id: UUID | None = None,
        status: SubscriptionStatusesEnum = SubscriptionStatusesEnum.ACTIVE,
    ):
        self._validate_subscription_period(pricing_plan, period)
        self._id = id
        self._studio_id = studio_id
        self._pricing_plan = pricing_plan
        self._period = period
        self._created_at = created_at
        self._updated_at = updated_at
        self._payment_id = payment_id
        self._status = status

    def _validate_subscription_period(
        self, pricing_plan: PricingPlanEnum, period: SubscriptionPeriod
    ) -> None:
        if pricing_plan == PricingPlanEnum.LIFETIME:
            if not period.is_unbounded:
                raise SubscriptionPeriodMustBeUnbounded(
                    "LIFETIME plan requires unbounded period (end_time must be None)"
                )
        if period.is_unbounded:
            raise SubscriptionPeriodMustBeBounded(
                f"{pricing_plan.value} plan requires bounded period (end_time must be set)"
            )

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def studio_id(self) -> UUID:
        return self._studio_id

    @property
    def pricing_plan(self) -> PricingPlanEnum:
        return self._pricing_plan

    @property
    def period(self) -> SubscriptionPeriod:
        return self._period

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def payment_id(self) -> UUID | None:
        return self._payment_id

    @property
    def status(self) -> SubscriptionStatusesEnum:
        return self._status

    def is_trial(self) -> bool:
        return self._pricing_plan == PricingPlanEnum.TRIAL

    def is_expired(self, current_time: datetime) -> bool:
        if self._period.end_time is None:
            return False
        return current_time > self._period.end_time

    def is_active(self) -> bool:
        return self._status == SubscriptionStatusesEnum.ACTIVE

    def is_lifetime(self) -> bool:
        return self._pricing_plan == PricingPlanEnum.LIFETIME

    def expire(self, expired_at: datetime):
        """Истекает подписку."""
        self._status = SubscriptionStatusesEnum.EXPIRED
        self._updated_at = expired_at

    def cancel(self, cancelled_at: datetime):
        """Отменяет подписку."""
        self._status = SubscriptionStatusesEnum.CANCELLED
        self._updated_at = cancelled_at

    def activate(self, activated_at: datetime):
        """Активирует подписку."""
        self._status = SubscriptionStatusesEnum.ACTIVE
        self._updated_at = activated_at
