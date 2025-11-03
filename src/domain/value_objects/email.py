import re

from ..errors import InvalidEmailError


class Email:
    """Value Object. Represents an email address."""

    __EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$)"

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise InvalidEmailError("Email value must be a string")
        if not re.match(self.__EMAIL_REGEX, value):
            raise InvalidEmailError(f"Invalid email address {value}")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Email):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value
