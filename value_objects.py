from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID
from enums import (
    CommunicationChannelsTypesEnum,
    FileTypesEnum,
    ProjectStatusesEnum,
    ServicesTypesEnum,
    SubProjectStatusesEnum,
    TaskStatusesEnum,
)


@dataclass(frozen=True)
class CommunicationChannel:
    """
    This class represents the low level priority communication methods.
    value is id of social profile
    """

    type: CommunicationChannelsTypesEnum
    value: str | None = None
    username: str | None = None


@dataclass(frozen=True)
class ContactInfo:
    """
    This class represents the high level priority communication methods.
    """

    phone: str
    email: str | None = None
    additional_channels: List[CommunicationChannel] | None = field(default_factory=list)


@dataclass(frozen=True)
class PersonalInfo:
    first_name: str
    last_name: str
    patronymic: str | None = None
    avatar_url: str | None = None
    bio: str | None = None


@dataclass(frozen=True)
class EmployeeInfo:
    specialties: List[ServicesTypesEnum]
    hourly_rate: Decimal
    portfolio_url: str | None = None


@dataclass
class DesignStyle:
    id: UUID
    name: str


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
    description: str | None = None
    status: TaskStatusesEnum = TaskStatusesEnum.NEW
    completed_at: datetime | None = None


@dataclass
class File:
    id: UUID
    project_id: UUID
    subproject_id: UUID | None
    uploaded_by: UUID
    file_type: FileTypesEnum
    format: str  # can be property cause we have AudioFormatsEnum and etc?
    url: str
    uploaded_at: datetime


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
    service_type: ServicesTypesEnum
    status: SubProjectStatusesEnum = SubProjectStatusesEnum.ASSIGNED
    tasks: List[Task] = field(default_factory=list)


@dataclass
class Comment:
    id: UUID
    project_id: UUID
    left_by: UUID  # it can be owner or client
    text: str
    created_at: datetime


@dataclass
class Project:
    """
    This class represents the agregated root of subprojects.
    """

    id: UUID
    studio_id: UUID
    client_id: UUID
    created_by: UUID
    service_type: ServicesTypesEnum
    subprojects: List[SubProject] = field(default_factory=list)
    status: ProjectStatusesEnum = ProjectStatusesEnum.DRAFT
