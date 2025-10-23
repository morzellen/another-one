from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ..enums import PricingPlanEnum, SubscriptionStatusesEnum
from ..value_objects.value_objects import TimeRange


@dataclass
class Subscription:
    """
    Это план подписки для студии.
    Привязывается к студии при создании, включая пробные периоды (без необходимости оплаты).
    Пробные периоды рассматриваются как активные подписки с фиксированным сроком и без payment_id.
    """

    id: UUID
    studio_id: UUID  # studio linked to a subscription
    pricing_plan: PricingPlanEnum
    period: TimeRange

    created_at: datetime
    updated_at: datetime

    payment_id: UUID | None = None  # link to the payment
    status: SubscriptionStatusesEnum = SubscriptionStatusesEnum.ACTIVE

    def is_active(self) -> bool:
        return self.status == SubscriptionStatusesEnum.ACTIVE

    def is_trial(self) -> bool:
        return self.pricing_plan == PricingPlanEnum.TRIAL

    def is_expired(self) -> bool:
        if self.period.end is None:
            return False
        return datetime.now() > self.period.end
