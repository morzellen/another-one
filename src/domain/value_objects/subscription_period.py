from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..errors import InvalidSubscriptionPeriodError


@dataclass(frozen=True)
class SubscriptionPeriod:
    """
    Value Object for subscription periods (bounded or unbounded).
    NO DEPENDENCY ON ENUMS OR EXTERNAL BUSINESS LOGIC.

    Business rules encapsulated here:
    - If end_time is None → unbounded period (infinite)
    - If end_time is set → must be after start_time

    Usage:
        # In Subscription entity:
        if pricing_plan == PricingPlanEnum.LIFETIME:
            period = SubscriptionPeriod(start_time=now)  # end_time=None by default
        else:
            period = SubscriptionPeriod(start_time=now, end_time=now + duration)

    Example (unbounded):
        lifetime = SubscriptionPeriod(start_time=datetime(2024, 1, 1))

    Example (bounded):
        trial = SubscriptionPeriod(
            start_time=datetime(2024, 1, 1),
            end_time=datetime(2024, 1, 15)
        )
    """

    start_time: datetime
    end_time: Optional[datetime] = None

    def __post_init__(self):
        """Validate core invariants of time period."""
        if self.end_time is not None and self.end_time <= self.start_time:
            raise InvalidSubscriptionPeriodError(
                f"Invalid period: end_time ({self.end_time}) must be after start_time ({self.start_time})"
            )

    @property
    def is_unbounded(self) -> bool:
        """Check if period has no defined end (infinite duration)."""
        return self.end_time is None

    def contains(self, time: datetime) -> bool:
        """Check if time is covered by period."""
        if self.is_unbounded:
            return time >= self.start_time
        return self.start_time <= time <= self.end_time

    def __str__(self) -> str:
        end_str = "∞" if self.is_unbounded else self.end_time.strftime("%Y-%m-%d")
        return f"{self.start_time.strftime('%Y-%m-%d')} → {end_str}"

    def __repr__(self) -> str:
        end_repr = "None" if self.is_unbounded else self.end_time.isoformat()
        return (
            f"SubscriptionPeriod("
            f"start_time={self.start_time.isoformat()}, "
            f"end_time={end_repr})"
        )
