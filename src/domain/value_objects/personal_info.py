import re
from ..errors import InvalidPersonalInfoError


class PersonalInfo:
    """
    Value Object. Represents personal info, which is part of any user profile.
    """

    __URL_REGEX = r"^https?://[^\s/$.?#].[^\s]*$"

    def __init__(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        patronymic: str | None = None,
        avatar_url: str | None = None,
        bio: str | None = None,
    ):
        self._first_name = self._validate_name_field(first_name, "First name")
        self._last_name = self._validate_name_field(last_name, "Last name")
        self._patronymic = self._validate_name_field(patronymic, "Patronymic")
        self._avatar_url = self._validate_url(avatar_url, "Avatar URL")
        self._bio = self._validate_name_field(bio, "Bio")

    @property
    def first_name(self) -> str | None:
        return self._first_name

    @property
    def last_name(self) -> str | None:
        return self._last_name

    @property
    def patronymic(self) -> str | None:
        return self._patronymic

    @property
    def avatar_url(self) -> str | None:
        return self._avatar_url

    @property
    def bio(self) -> str | None:
        return self._bio

    def _validate_name_field(self, field: str | None, field_name: str) -> str | None:
        """Validates a name field."""
        if field is not None and not field.strip():
            raise InvalidPersonalInfoError(f"{field_name} cannot be an empty string")
        return field.strip() if field else field

    def _validate_url(self, url: str | None, url_name: str) -> str | None:
        """Validates a URL field."""
        if url is not None and not re.match(self.__URL_REGEX, url):
            raise InvalidPersonalInfoError(
                f"{url_name} must be a valid URL starting with http:// or https://"
            )
        return url

    def __eq__(self, other) -> bool:
        if not isinstance(other, PersonalInfo):
            return False
        return (
            self._first_name == other._first_name
            and self._last_name == other._last_name
            and self._patronymic == other._patronymic
            and self._avatar_url == other._avatar_url
            and self._bio == other._bio
        )

    def __hash__(self) -> int:
        return hash(
            (self._first_name, self._last_name, self._patronymic, self._avatar_url, self._bio)
        )

    def get_full_name(self) -> str:
        """Returns the full name of the person."""
        parts = [part for part in [self._first_name, self._patronymic, self._last_name] if part]
        return " ".join(parts) if parts else ""
