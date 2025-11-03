import re
from ..errors import InvalidStudioConfigurationError
from .discount_policy import DiscountPolicy


class StudioConfiguration:
    """
    Value Object. Represents studio configuration.
    All fields are optional, but if present they must be valid.
    Used to pass configuration between layers (e.g., from controller to service).
    """

    __URL_REGEX = r"^https?://[^\s/$.?#].[^\s]*$"

    def __init__(
        self,
        description: str | None = None,
        logo_url: str | None = None,
        discount_policy: DiscountPolicy | None = None,
    ):
        self._description = self._validate_description(description)
        self._logo_url = self._validate_url(logo_url)
        self._discount_policy = discount_policy

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def logo_url(self) -> str | None:
        return self._logo_url

    @property
    def discount_policy(self) -> DiscountPolicy | None:
        return self._discount_policy

    def _validate_description(self, description: str | None) -> str | None:
        """Validates the description."""
        if description is not None:
            if not description.strip():
                raise InvalidStudioConfigurationError("Description cannot be empty or whitespace")
        return description

    def _validate_url(self, url: str | None) -> str | None:
        """Validates the URL."""
        if url is not None:
            if not re.match(self.__URL_REGEX, url):
                raise InvalidStudioConfigurationError("Logo URL must be a valid HTTP/HTTPS URL")
        return url

    def __eq__(self, other) -> bool:
        if not isinstance(other, StudioConfiguration):
            return False
        return (
            self._description == other._description
            and self._logo_url == other._logo_url
            and self._discount_policy == other._discount_policy
        )

    def __hash__(self) -> int:
        return hash((self._description, self._logo_url, self._discount_policy))

    def has_discount_policy(self) -> bool:
        """Checks if the configuration has a discount policy."""
        return self._discount_policy is not None
