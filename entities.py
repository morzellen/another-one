from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Set
from uuid import UUID
from enums import (
    AuthProviderEnum,
    BookingStatusesEnum,
    CommunicationChannelsTypesEnum,
    FileFormatEnum,
    FileTypesEnum,
    PaymentMethodsEnum,
    PaymentStatusesEnum,
    ProjectStatusesEnum,
    ServicesTypesEnum,
    ServicesTypesForBookingEnum,
    SubProjectStatusesEnum,
    TaskStatusesEnum,
    UserRoleEnum,
    UserStatusesEnum,
)
from value_objects import ContactInfo, EmployeeInfo, PersonalInfo


@dataclass
class Booking:
    """
    This class represents a studio booking in the recording studio management platform.
    Bookings are used to schedule services for clients, such as mixing,
    mastering, recording and etc.
    It can be created by clients and confirmed by studio owners.
    It can be linked to an existing project and its subprojects, or not linked at all.
    Client can reschedule the booking by himself, but only if it is confirmed by
    the owner/the person responsible for it. Otherwise, he may return to the time that
    was agreed upon.
    """

    id: UUID
    studio_id: UUID
    client_id: UUID
    service_type: ServicesTypesForBookingEnum
    start_time: datetime
    end_time: datetime
    assigned_employee_id: UUID  # specialist id who is assigned to this booking

    created_at: datetime
    updated_at: datetime | None = None

    confirmed_at: datetime | None = None
    cancelled_at: datetime | None = None
    completed_at: datetime | None = None
    rescheduled_at: datetime | None = None

    project_id: UUID | None = None  # can be not linked to a project

    status: BookingStatusesEnum = BookingStatusesEnum.CREATED
    payment_status: PaymentStatusesEnum = PaymentStatusesEnum.UNPAID
    payment_method: PaymentMethodsEnum = PaymentMethodsEnum.CASH


@dataclass
class DiscountPolicy:
    """
    This class represents a discount policy in the recording studio management platform.
    This will be used to apply discounts to clients based on their track statistics.
    It's configured by the studio owner.
    """

    studio_id: UUID
    discount_percent: Decimal  # 0.1 = 10%
    required_status: UserStatusesEnum | None
    min_tracks: int | None
    period_days: int | None
    created_at: datetime
    updated_at: datetime | None = None


@dataclass
class Studio:
    """
    This class represents a recording studio in the recording studio management platform.
    Studios are the central locations where clients can create projects, services and etc.
    Studios are managed by owners and have a unique identifier (UUID).
    It's the main part of the SaaS system, where everything happens.
    """

    id: UUID
    owner_id: UUID
    name: str
    discount_policy: DiscountPolicy
    created_at: datetime
    updated_at: datetime | None = None


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
    9. Set up his personal info (base personal info like name, email, phone, avatar, etc)
    10. Add comment to project (it means what client wants to see in track, cover or etc)
    11. Add services to project like promotion, create cover design, etc. It will be automatically created as a subproject.
    12. Upload sound/image to subproject (what client wants to see/hear in track or cover)
    """

    user_id: UUID


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
    6. Set up his personal info (base personal info, price for services, etc)
    7. Add task to subproject
    8. Change task status in subproject
    9. Notificate/send message to client about whatever
    """

    user_id: UUID
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
    6. Set up his personal info (base personal info, price for services, etc)
    7. Add task to subproject
    8. Change task status in subproject
    9. Notificate/send message to client about whatever
    """

    user_id: UUID
    employee_info: EmployeeInfo
    design_style_ids: List[UUID] = field(default_factory=list)


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

    user_id: UUID


@dataclass
class AuthIdentity:
    user_id: UUID
    provider: AuthProviderEnum
    provider_user_id: str


@dataclass
class User:
    id: UUID
    studio_id: UUID
    contact_info: ContactInfo
    personal_info: PersonalInfo
    status: UserStatusesEnum
    roles: Set[UserRoleEnum]

    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    created_from_oauth: bool = False
    has_custom_profile: bool = False  # did the user edit the profile manually?


@dataclass()
class CommunicationChannel:
    """
    This class represents the low level priority communication methods.
    value is id of social profile
    """

    id: UUID
    user_id: UUID
    type: CommunicationChannelsTypesEnum
    created_at: datetime
    value: str | None = None
    username: str | None = None


@dataclass
class DesignStyle:
    """
    This class represents the design style, which is part of designer profile.
    It can be a name of style like minimalistic, modern, etc.
    """

    id: UUID
    studio_id: UUID
    name: str
    created_at: datetime


@dataclass
class Task:
    """
    This class represents the task, wich is part of subproject and the employee
    assigns to himself.
    """

    id: UUID
    subproject_id: UUID
    title: str
    created_by: UUID  # engineer/designer
    created_at: datetime
    updated_at: datetime | None = None

    description: str | None = None
    status: TaskStatusesEnum = TaskStatusesEnum.NEW
    completed_at: datetime | None = None


@dataclass
class File:
    """
    This class represents the file, which is part of project.
    It can be audio, video or image and can be uploaded by employee or client.
    """

    id: UUID
    project_id: UUID
    subproject_id: UUID | None
    uploaded_by: UUID
    uploaded_at: datetime

    file_type: FileTypesEnum
    format: FileFormatEnum
    url: str

    archived_at: datetime | None = None


@dataclass
class SubProject:
    """
    This class represents the agregated root of tasks.
    """

    id: UUID
    studio_id: UUID
    project_id: UUID
    created_by: (
        UUID  # who created subproject and working with it (only emplyoee can do that)
    )
    updated_at: datetime
    service_type: ServicesTypesEnum
    booking_id: UUID | None = None

    status: SubProjectStatusesEnum = SubProjectStatusesEnum.ASSIGNED
    tasks_ids: List[UUID] = field(default_factory=list)
    files_ids: List[UUID] = field(default_factory=list)

    completed_at: datetime | None = None


@dataclass
class Comment:
    """
    This class represents the comment to project. It can be left by owner or client.
    We can consider this a note that a client or studio owner creates, and those
    who work on the project will see it.
    """

    id: UUID
    studio_id: UUID
    project_id: UUID
    left_by: UUID  # it can be owner or client
    text: str
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


@dataclass
class Project:
    """
    This class represents the agregated root of subprojects.
    The project is a kind of work space with studio services, in which the client
    monitors the changes made by the employees.
    He can also create this project for the future, or book time for an existing one.
    Also project can be archived when it is completed and no longer active.
    Project can be created by client or studio owner.
    """

    id: UUID
    studio_id: UUID
    client_id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None = None

    status: ProjectStatusesEnum = ProjectStatusesEnum.DRAFT
    subprojects_ids: List[UUID] = field(default_factory=list)
    comments_ids: List[UUID] = field(default_factory=list)
    files_ids: List[UUID] = field(default_factory=list)

    completed_at: datetime | None = None
    archived_at: datetime | None = None
