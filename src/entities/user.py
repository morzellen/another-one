from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ..value_objects.value_objects import ContactInfo, PersonalInfo


@dataclass
class User:
    """
    Global user identity. Represents a human across the entire platform.
    Does NOT belong to any studio by default.
    Does NOT contain authentication details.
    Becomes associated with studios via UserStudioMembership.
    """

    id: UUID
    contact_info: ContactInfo

    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    personal_info: PersonalInfo | None = None

    created_from_oauth: bool = False  # do we need this field in User?
    has_custom_profile: bool = False  # did the user edit the profile manually?
