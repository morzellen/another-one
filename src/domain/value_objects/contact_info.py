from uuid import UUID
from ..errors import InvalidContactInfoError
from .email import Email
from .phone import Phone


class ContactInfo:
    """
    Value Object. Represents high level priority communication methods.
    At least one communication channel must be required.
    """

    def __init__(
        self,
        phone: Phone | None = None,
        email: Email | None = None,
        additional_channels_ids: tuple[UUID, ...] | None = None,
    ):
        self._phone = phone
        self._email = email
        self._additional_channels_ids = additional_channels_ids or tuple()

        # Validate that at least one communication channel is provided
        if not self._has_any_channel():
            raise InvalidContactInfoError(
                "At least one communication channel must be provided: "
                "either 'phone', 'email', or 'additional_channels_ids'."
            )

    @property
    def phone(self) -> Phone | None:
        return self._phone

    @property
    def email(self) -> Email | None:
        return self._email

    @property
    def additional_channels_ids(self) -> tuple[UUID, ...]:
        return self._additional_channels_ids

    def _has_any_channel(self) -> bool:
        """Checks if any communication channel is provided."""
        return (
            self._phone is not None
            or self._email is not None
            or len(self._additional_channels_ids) > 0
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, ContactInfo):
            return False
        return (
            self._phone == other._phone
            and self._email == other._email
            and self._additional_channels_ids == other._additional_channels_ids
        )

    def __hash__(self) -> int:
        return hash((self._phone, self._email, self._additional_channels_ids))

    def has_phone(self) -> bool:
        """Checks if phone is provided."""
        return self._phone is not None

    def has_email(self) -> bool:
        """Checks if email is provided."""
        return self._email is not None

    def has_additional_channels(self) -> bool:
        """Checks if additional channels are provided."""
        return len(self._additional_channels_ids) > 0
