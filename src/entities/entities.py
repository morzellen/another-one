from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from ..enums import (
    BookingStatusesEnum,
    CommunicationChannelsTypesEnum,
    FileFormatEnum,
    FileTypesEnum,
    PaymentMethodsEnum,
    PaymentStatusesEnum,
    ProjectStatusesEnum,
    ServicesTypesEnum,
    SubProjectStatusesEnum,
    TaskStatusesEnum,
)
from ..value_objects.value_objects import TimeRange
from ..constants import BOOKING_ALLOWED_SERVICES


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

    Note:
        The `service_type` must be one of the services allowed for booking.
        See `BOOKING_ALLOWED_SERVICES` for the valid options.
    """

    id: UUID
    studio_id: UUID
    client_id: UUID
    assigned_employee_id: UUID  # specialist id who is assigned to this booking
    service_type: ServicesTypesEnum
    time_range: TimeRange

    created_at: datetime

    confirmed_at: datetime | None = None
    cancelled_at: datetime | None = None
    completed_at: datetime | None = None
    rescheduled_at: datetime | None = None

    project_id: UUID | None = None  # can be not linked to a project

    status: BookingStatusesEnum = BookingStatusesEnum.CREATED
    payment_status: PaymentStatusesEnum = PaymentStatusesEnum.PENDING
    payment_method: PaymentMethodsEnum = PaymentMethodsEnum.CASH

    def __post_init__(self) -> None:
        """Validate that the service_type is allowed for booking."""
        if self.service_type not in BOOKING_ALLOWED_SERVICES:
            raise ValueError(
                f"Service '{self.service_type.value}' is not allowed for booking. "
                f"Allowed services: {[service.value for service in BOOKING_ALLOWED_SERVICES]}"
            )


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
    project_id: UUID
    created_by: (
        UUID  # who created subproject and working with it (only emplyoee can do that)
    )
    updated_at: datetime
    service_type: ServicesTypesEnum
    booking_id: UUID | None = None

    status: SubProjectStatusesEnum = SubProjectStatusesEnum.ASSIGNED
    tasks_ids: list[UUID] = field(default_factory=list)
    files_ids: list[UUID] = field(default_factory=list)

    completed_at: datetime | None = None


@dataclass
class Comment:
    """
    This class represents the comment to project. It can be left by owner or client.
    We can consider this a note that a client or studio owner creates, and those
    who work on the project will see it.
    """

    id: UUID
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
    subprojects_ids: list[UUID] = field(default_factory=list)
    comments_ids: list[UUID] = field(default_factory=list)
    files_ids: list[UUID] = field(default_factory=list)

    completed_at: datetime | None = None
    archived_at: datetime | None = None
