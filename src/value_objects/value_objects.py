import re
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from ..enums import ServicesTypesEnum, UserStatusesEnum
from ..errors import (
    InvalidContactInfoError,
    InvalidEmailError,
    InvalidEmployeeInfoError,
    InvalidPersonalInfoError,
    InvalidPhoneError,
    InvalidTimeRangeError,
)


@dataclass(frozen=True)
class Email:
    value: str

    __EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$)"

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise InvalidEmailError("Email value must be a string")
        if not re.match(self.__EMAIL_REGEX, self.value):
            raise InvalidEmailError(f"Invalid email address {self.value}")


@dataclass(frozen=True)
class Phone:
    value: str

    __PHONE_REGEX = r"^\+?\d{1,4}[-.\s]?\d{9,15}$"

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise InvalidPhoneError("Phone value must be a string")
        if not re.match(self.__PHONE_REGEX, self.value):
            raise InvalidPhoneError(f"Invalid phone number {self.value}")


@dataclass(frozen=True)
class ContactInfo:
    """
    This class represents the high level priority communication methods.
    At least one communication channel must be required!!!
    """

    phone: Phone | None = None
    email: Email | None = None
    additional_channels_ids: tuple[UUID, ...] | None = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """
        Validates that at least one communication channel is provided.
        """
        if not (
            self.phone
            or self.email
            or (self.additional_channels_ids and len(self.additional_channels_ids) > 0)
        ):
            raise InvalidContactInfoError(
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

    __URL_REGEX = r"^https?://[^\s/$.?#].[^\s]*$"

    def __post_init__(self) -> None:
        if self.first_name is not None and not self.first_name.strip():
            raise InvalidPersonalInfoError("First name cannot be an empty string")
        if self.last_name is not None and not self.last_name.strip():
            raise InvalidPersonalInfoError("Last name cannot be an empty string")
        if self.patronymic is not None and not self.patronymic.strip():
            raise InvalidPersonalInfoError("Patronymic cannot be an empty string")
        if self.bio is not None and not self.bio.strip():
            raise InvalidPersonalInfoError("Bio cannot be an empty string")
        if self.avatar_url is not None and not re.match(
            self.__URL_REGEX, self.avatar_url
        ):
            raise InvalidPersonalInfoError(
                "Avatar URL must be a valid URL starting with http:// or https://"
            )


@dataclass(frozen=True)
class EmployeeInfo:
    """
    This class represents the employee info, which is part of engineer or designer profile.
    """

    specialties: tuple[ServicesTypesEnum, ...]
    hourly_rate: Decimal
    portfolio_url: str | None = None

    __URL_REGEX = r"^https?://[^\s/$.?#].[^\s]*$"

    def __post_init__(self) -> None:
        if self.hourly_rate < 0:
            raise InvalidEmployeeInfoError("Hourly rate cannot be negative")
        if not self.specialties or len(self.specialties) == 0:
            raise InvalidEmployeeInfoError("Employee must have at least one specialty")
        if self.portfolio_url is not None and not re.match(
            self.__URL_REGEX, self.portfolio_url
        ):
            raise InvalidEmployeeInfoError(
                "Portfolio URL must be a valid URL starting with http:// or https://"
            )


@dataclass(frozen=True)
class TimeRange:
    """
    This class represents the time range, which is part of booking or subscription.
    """

    start_time: datetime
    end_time: datetime

    def __post_init__(self) -> None:
        if self.end_time <= self.start_time:
            raise InvalidTimeRangeError("TimeRange must have end_time > start_time")


@dataclass(frozen=True)
class DiscountPolicy:
    """
    This class represents a discount policy in the recording studio management platform.
    This will be used to apply discounts to clients based on their track statistics.
    It's configured by the studio owner.
    """

    studio_id: UUID
    discount_percent: Decimal  # 0.1 = 10%
    min_tracks: int | None
    period_days: int | None
    created_at: datetime
    updated_at: datetime | None = None
    required_status: UserStatusesEnum = (
        UserStatusesEnum.VIP
    )  # this is the one who is covered by the discount

    def __post_init__(self):
        """Ensure immutability and validation on creation."""
        object.__setattr__(self, "updated_at", self.updated_at or self.created_at)

        if self.discount_percent < 0 or self.discount_percent > 1:
            raise InvalidDiscountPolicyError("Discount percent must be between 0 and 1")

    def apply_to_user(self, user_status: UserStatusesEnum, track_count: int) -> Decimal:
        """
        Применяет скидку к пользователю.
        Возвращает процент скидки (0.0 - 1.0).
        """
        if user_status != self.required_status:
            return Decimal("0.0")

        if self.min_tracks and track_count < self.min_tracks:
            return Decimal("0.0")

        # period_days — требует дополнительной логики, не реализуем здесь
        return self.discount_percent

    def is_applicable(self, user_status: UserStatusesEnum, track_count: int) -> bool:
        return self.apply_to_user(user_status, track_count) > 0


@dataclass(frozen=True)
class StudioConfiguration:
    """
    Value Object. Представляет конфигурацию студии.
    Все поля необязательны, но при их наличии они должны быть валидными.
    Используется для передачи конфигурации между слоями (например, от контроллера к сервису).
    """

    name: str | None = None
    discount_policy: DiscountPolicy | None = None
    description: str | None = None
    logo_url: str | None = None

    __URL_REGEX = r"^https?://[^\s/$.?#].[^\s]*$"

    def __post_init__(self):
        """Валидация всех полей при создании."""
        if self.name is not None:
            if not self.name.strip():
                raise InvalidStudioConfigurationError(
                    "Studio name cannot be empty or whitespace"
                )
        if self.description is not None:
            if not self.description.strip():
                raise InvalidStudioConfigurationError(
                    "Description cannot be empty or whitespace"
                )
        if self.logo_url is not None:
            if not re.match(self.__URL_REGEX, self.logo_url):
                raise InvalidStudioConfigurationError(
                    "Logo URL must be a valid HTTP/HTTPS URL"
                )
