from datetime import datetime
from uuid import UUID

from ..value_objects.contact_info import ContactInfo
from ..value_objects.personal_info import PersonalInfo


class User:
    """
    Global user identity. Represents a human across the entire platform.
    Does NOT belong to any studio by default.
    Does NOT contain authentication details.
    Becomes associated with studios via UserStudioMembership.
    """

    def __init__(
        self,
        id: UUID,
        contact_info: ContactInfo,
        created_at: datetime,
        updated_at: datetime | None = None,
        deleted_at: datetime | None = None,
        personal_info: PersonalInfo | None = None,
        created_from_oauth: bool = False,
        has_custom_profile: bool = False,
    ):
        self._id = id
        self._contact_info = contact_info
        self._created_at = created_at
        self._updated_at = updated_at
        self._deleted_at = deleted_at
        self._personal_info = personal_info
        self._created_from_oauth = created_from_oauth
        self._has_custom_profile = has_custom_profile

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def contact_info(self) -> ContactInfo:
        return self._contact_info

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    @property
    def deleted_at(self) -> datetime | None:
        return self._deleted_at

    @property
    def personal_info(self) -> PersonalInfo | None:
        return self._personal_info

    @property
    def created_from_oauth(self) -> bool:
        return self._created_from_oauth

    @property
    def has_custom_profile(self) -> bool:
        return self._has_custom_profile

    def is_deleted(self) -> bool:
        return self._deleted_at is not None

    def update_contact_info(self, new_contact_info: ContactInfo):
        """Обновляет контактную информацию пользователя."""
        if not isinstance(new_contact_info, ContactInfo):
            raise ValueError("Contact info must be a ContactInfo instance")
        self._contact_info = new_contact_info
        self._updated_at = datetime.now()

    def update_personal_info(self, new_personal_info: PersonalInfo):
        """Обновляет персональную информацию пользователя."""
        if new_personal_info is not None and not isinstance(new_personal_info, PersonalInfo):
            raise ValueError("Personal info must be a PersonalInfo instance or None")
        self._personal_info = new_personal_info
        self._updated_at = datetime.now()

    def soft_delete(self):
        """Мягкое удаление пользователя."""
        self._deleted_at = datetime.now()
        self._updated_at = datetime.now()

    def restore(self):
        """Восстановление пользователя."""
        self._deleted_at = None
        self._updated_at = datetime.now()
