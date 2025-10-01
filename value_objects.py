from dataclasses import dataclass, field
from decimal import Decimal
from typing import List
from uuid import UUID
from enums import ServicesTypesEnum


@dataclass()
class ContactInfo:
    """
    This class represents the high level priority communication methods.
    At least one communication channel must be required!!!
    """

    phone: str | None = None
    email: str | None = None
    additional_channels_ids: List[UUID] | None = field(default_factory=list)


@dataclass()
class PersonalInfo:
    """
    This class represents the personal info, which is part of any user profile.
    """

    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    avatar_url: str | None = None
    bio: str | None = None


@dataclass()
class EmployeeInfo:
    """
    This class represents the employee info, which is part of engineer or designer profile.
    """

    specialties: List[ServicesTypesEnum]
    hourly_rate: Decimal
    portfolio_url: str | None = None
