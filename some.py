# Можно ли сделать это так?
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Set
from uuid import UUID

from enums import ServicesTypesEnum, UserRoleEnum, UserStatusesEnum


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


@dataclass
class User:
    id: UUID
    studio_id: UUID
    contact_info: ContactInfo
    personal_info: PersonalInfo
    status: UserStatusesEnum
    profiles: Set[UserRoleEnum]

    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    
    
# class Employee


@dataclass()
class EmployeeInfo:
    """
    This class represents the employee info, which is part of engineer or designer profile.
    """

    specialties: List[ServicesTypesEnum]
    hourly_rate: Decimal
    portfolio_url: str | None = None


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
    
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    
    created_from_oauth: bool = False
    has_custom_profile: bool = False  # did the user edit the profile manually?


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
