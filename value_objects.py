from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from enums import ServicesTypesEnum


@dataclass(frozen=True)
class ContactInfo:
    """
    This class represents the high level priority communication methods.
    At least one communication channel must be required!!!
    """

    phone: str | None = None
    email: str | None = None
    additional_channels_ids: tuple[UUID, ...] | None = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """
        Validates that at least one communication channel is provided.
        """
        if (
            not (self.phone and self.phone.strip())
            and not (self.email and self.email.strip())
            and (
                not self.additional_channels_ids
                or len(self.additional_channels_ids) == 0
            )
        ):
            raise ValueError(
                "At least one communication channel must be provided: "
                "either 'phone', 'email', or 'additional_channels_ids'."
            )


@dataclass(frozen=True)
class PersonalInfo:
    """
    This class represents the personal info, which is part of any user profile.
    """

    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    avatar_url: str | None = None
    bio: str | None = None


@dataclass(frozen=True)
class EmployeeInfo:
    """
    This class represents the employee info, which is part of engineer or designer profile.
    """

    specialties: tuple[ServicesTypesEnum, ...]
    hourly_rate: Decimal
    portfolio_url: str | None = None


@dataclass(frozen=True)
class TimeRange:
    """
    This class represents the time range, which is part of booking.
    """

    start_time: datetime
    end_time: datetime
