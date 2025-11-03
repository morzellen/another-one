from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ..enums import UserStatusesEnum
from ..errors import InvalidDiscountPolicyError


class DiscountPolicy:
    """
    Value Object. Represents a discount policy in the recording studio management platform.
    This will be used to apply discounts to clients based on their track statistics.
    It's configured by the studio owner.
    """

    def __init__(
        self,
        studio_id: UUID,
        discount_percent: Decimal,  # 0.1 = 10%
        min_tracks: int | None,
        period_days: int | None,
        created_at: datetime,
        updated_at: datetime | None = None,
        required_status: UserStatusesEnum = UserStatusesEnum.VIP,
    ):
        if discount_percent < 0 or discount_percent > 1:
            raise InvalidDiscountPolicyError("Discount percent must be between 0 and 1")

        self._studio_id = studio_id
        self._discount_percent = discount_percent
        self._min_tracks = min_tracks
        self._period_days = period_days
        self._created_at = created_at
        self._updated_at = updated_at or created_at
        self._required_status = required_status

    @property
    def studio_id(self) -> UUID:
        return self._studio_id

    @property
    def discount_percent(self) -> Decimal:
        return self._discount_percent

    @property
    def min_tracks(self) -> int | None:
        return self._min_tracks

    @property
    def period_days(self) -> int | None:
        return self._period_days

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def required_status(self) -> UserStatusesEnum:
        return self._required_status

    def apply_to_user(self, user_status: UserStatusesEnum, track_count: int) -> Decimal:
        """
        Applies discount to user.
        Returns the discount percentage (0.0 - 1.0).
        """
        if user_status != self._required_status:
            return Decimal("0.0")
        if self._min_tracks and track_count < self._min_tracks:
            return Decimal("0.0")
        # period_days — requires additional logic, not implemented here
        return self._discount_percent

    def is_applicable(self, user_status: UserStatusesEnum, track_count: int) -> bool:
        return self.apply_to_user(user_status, track_count) > 0

    def __eq__(self, other) -> bool:
        if not isinstance(other, DiscountPolicy):
            return False
        return (
            self._studio_id == other._studio_id
            and self._discount_percent == other._discount_percent
            and self._min_tracks == other._min_tracks
            and self._period_days == other._period_days
            and self._required_status == other._required_status
        )

    def __hash__(self) -> int:
        return hash(
            (
                self._studio_id,
                self._discount_percent,
                self._min_tracks,
                self._period_days,
                self._required_status,
            )
        )

    def update_discount_percent(self, new_discount_percent: Decimal) -> "DiscountPolicy":
        """Creates a new DiscountPolicy with updated discount percent."""
        if new_discount_percent < 0 or new_discount_percent > 1:
            raise InvalidDiscountPolicyError("Discount percent must be between 0 and 1")

        return DiscountPolicy(
            studio_id=self._studio_id,
            discount_percent=new_discount_percent,
            min_tracks=self._min_tracks,
            period_days=self._period_days,
            created_at=self._created_at,
            updated_at=datetime.now(),
            required_status=self._required_status,
        )
