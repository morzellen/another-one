from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Set
from uuid import UUID
from enums import (
    BookingStatusesEnum,
    PaymentMethodsEnum,
    PaymentStatusesEnum,
    ServicesTypesEnum,
    UserRoleEnum,
    UserStatusesEnum,
)
from value_objects import ContactInfo, DesignStyle, EmployeeInfo, PersonalInfo


@dataclass
class Booking:
    id: UUID
    studio_id: UUID
    client_id: UUID
    service_type: ServicesTypesEnum
    start_time: datetime
    end_time: datetime
    status: BookingStatusesEnum = BookingStatusesEnum.CREATED
    project_id: UUID | None = None  # can be not linked to a project
    payment_status: PaymentStatusesEnum = PaymentStatusesEnum.UNPAID
    payment_method: PaymentMethodsEnum | None = None


@dataclass
class Studio:
    id: UUID
    name: str


@dataclass
class DiscountPolicy:
    studio_id: UUID
    client_status: UserStatusesEnum = UserStatusesEnum.VIP
    min_tracks: int | None
    period_days: int | None
    discount_percent: Decimal  # 0.1 = 10%


@dataclass
class ClientProfile:
    """
    This class represents a client user in the recording studio management platform.

    Clients are the primary users who utilize studio services for their music and audio projects.
    They can create bookings for various services, manage their projects, upload and download files,
    communicate with studio staff, and track the progress of their work.

    What client can do:
    1. Create booking and choose service type to it like mixing, mastering, etc (automatically creating project)
    2. Create project, that he plans to implement
    3. Download file from project
    4. Upload file to project (whatever file)
    5. Delete file from project, which was uploaded by him
    7. Cancel booking
    8. Reschedule booking
    9. Set up his personal profile (base personal info like name, email, phone, avatar, etc)
    10. Add comment to project (it means what client wants to see in track, cover or etc)
    11. Choose services to project (promotion, create cover design, etc)
    12. Add sound/image uses AI to project (what client wants to see/hear in track or cover)
    """

    discount_tier: Decimal = Decimal("0.0")


@dataclass
class EngineerProfile:
    """
    This class represents an audio engineer user in the recording studio management platform.

    Engineers are specialized professionals who handle audio-related services such as mixing,
    mastering, and recording. They work on subprojects within larger client projects,
    managing audio files and completing specific technical tasks assigned to them.

    What engineer can do:
    ///Subproject is a part of project///

    1. Choose project and create his subproject
    2. Download file from subproject
    3. Upload file to subproject (mp3, wav)
    4. Delete file from subproject, which was uploaded by him
    5. Set status subproject is completed if all tasks are completed
    6. Set up his personal profile (base personal info, price for services, etc)
    7. Add task to subproject
    8. Change task status in subproject
    9. Notificate/send message to client about whatever
    """

    employee_info: EmployeeInfo


@dataclass
class DesignerProfile:
    """
    This class represents a designer user in the recording studio management platform.

    Designers are creative professionals who handle visual elements of projects such as album covers,
    promotional materials, and video content. They work on subprojects within larger client projects,
    managing visual files and completing design-related tasks assigned to them.

    What designer can do:
    ///Subproject is a part of project///

    1. Choose project and create his subproject
    2. Download file from subproject
    3. Upload file to subproject (jpg, png, mp4, avi)
    4. Delete file from subproject, which was uploaded by him
    5. Set status subproject is completed if all tasks are completed
    6. Set up his personal profile (base personal info, price for services, etc)
    7. Add task to subproject
    8. Change task status in subproject
    9. Notificate/send message to client about whatever
    """

    employee_info: EmployeeInfo
    design_styles: List[DesignStyle] = field(default_factory=list)


@dataclass
class OwnerProfile:
    """
    This class represents the studio owner/administrator in the recording studio management platform.

    Owners have full administrative privileges and can manage all aspects of the studio operations,
    including user management, project oversight, booking management, and system analytics.
    They have complete control over the platform and all its functionalities.

    What owner can do:
    ///Subproject is a part of project///

    1. Whatever he wants
    2. Create client in system
    3. Create employee in system
    4. Create projects/subprojects in system and link employees to it
    5. Set up personal profiles of users (base personal info, etc)
    6. Create/confirm/cancel/complete/reschedule booking in system
    7. Full control over statistics/analytics/activity
    8. Archive/unarchive project
    9. Notificate/send message to client about whatever
    10. Set price to services and add discount (discount depends on client's status or tracks/... statistics on some period)
    ...
    """


@dataclass
class User:
    id: UUID
    studio_id: UUID
    contact_info: ContactInfo
    personal_info: PersonalInfo
    status: UserStatusesEnum
    roles: Set[UserRoleEnum]
    # private fields for every profile
    _client_profile: ClientProfile | None = None
    _engineer_profile: EngineerProfile | None = None
    _designer_profile: DesignerProfile | None = None
    _owner_profile: OwnerProfile | None = None

    def __post_init__(self):
        # if we have a role, we must have a profile
        if UserRoleEnum.CLIENT in self.roles and self._client_profile is None:
            raise ValueError("User with CLIENT role must have a ClientProfile")
        if UserRoleEnum.ENGINEER in self.roles and self._engineer_profile is None:
            raise ValueError("User with ENGINEER role must have an EngineerProfile")
        if UserRoleEnum.DESIGNER in self.roles and self._designer_profile is None:
            raise ValueError("User with DESIGNER role must have a DesignerProfile")
        if UserRoleEnum.OWNER in self.roles and self._owner_profile is None:
            raise ValueError("User with OWNER role must have an OwnerProfile")

    def get_client_profile(self) -> ClientProfile | None:
        if UserRoleEnum.CLIENT not in self.roles:
            return None
        return self._client_profile

    def get_engineer_profile(self) -> EngineerProfile | None:
        if UserRoleEnum.ENGINEER not in self.roles:
            return None
        return self._engineer_profile

    def get_designer_profile(self) -> DesignerProfile | None:
        if UserRoleEnum.DESIGNER not in self.roles:
            return None
        return self._designer_profile

    def get_owner_profile(self) -> OwnerProfile | None:
        if UserRoleEnum.OWNER not in self.roles:
            return None
        return self._owner_profile
