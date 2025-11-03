from datetime import datetime
from uuid import UUID
from ..enums import CommunicationChannelsTypesEnum


class CommunicationChannel:
    """
    Entity. Represents a communication method for a user.
    value is id of social profile
    """

    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        type: CommunicationChannelsTypesEnum,
        created_at: datetime,
        value: str | None = None,
        username: str | None = None,
    ):
        self._id = id
        self._user_id = user_id
        self._type = type
        self._created_at = created_at
        self._value = value
        self._username = username

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def type(self) -> CommunicationChannelsTypesEnum:
        return self._type

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def value(self) -> str | None:
        return self._value

    @property
    def username(self) -> str | None:
        return self._username

    def update_value(self, new_value: str | None):
        """Updates the channel value."""
        self._value = new_value

    def update_username(self, new_username: str | None):
        """Updates the channel username."""
        self._username = new_username
