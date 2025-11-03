import re
from decimal import Decimal
from ..enums import ServicesTypesEnum
from ..errors import InvalidEmployeeInfoError


class EmployeeInfo:
    """
    Value Object. Represents employee info, which is part of engineer or designer profile.
    """

    __URL_REGEX = r"^https?://[^\s/$.?#].[^\s]*$"

    def __init__(
        self,
        specialties: tuple[ServicesTypesEnum, ...],
        hourly_rate: Decimal,
        portfolio_url: str | None = None,
    ):
        if hourly_rate < 0:
            raise InvalidEmployeeInfoError("Hourly rate cannot be negative")
        if not specialties or len(specialties) == 0:
            raise InvalidEmployeeInfoError("Employee must have at least one specialty")

        self._specialties = tuple(specialties)  # Ensure it's a tuple
        self._hourly_rate = hourly_rate
        self._portfolio_url = self._validate_url(portfolio_url)

    @property
    def specialties(self) -> tuple[ServicesTypesEnum, ...]:
        return self._specialties

    @property
    def hourly_rate(self) -> Decimal:
        return self._hourly_rate

    @property
    def portfolio_url(self) -> str | None:
        return self._portfolio_url

    def _validate_url(self, url: str | None) -> str | None:
        """Validates the portfolio URL."""
        if url is not None and not re.match(self.__URL_REGEX, url):
            raise InvalidEmployeeInfoError(
                "Portfolio URL must be a valid URL starting with http:// or https://"
            )
        return url

    def __eq__(self, other) -> bool:
        if not isinstance(other, EmployeeInfo):
            return False
        return (
            self._specialties == other._specialties
            and self._hourly_rate == other._hourly_rate
            and self._portfolio_url == other._portfolio_url
        )

    def __hash__(self) -> int:
        return hash((self._specialties, self._hourly_rate, self._portfolio_url))

    def has_specialty(self, specialty: ServicesTypesEnum) -> bool:
        """Checks if the employee has a specific specialty."""
        return specialty in self._specialties
