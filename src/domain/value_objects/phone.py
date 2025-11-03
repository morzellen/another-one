import re

from ..errors import InvalidPhoneError


class Phone:
    """Value Object. Represents a phone number."""

    __PHONE_REGEX = r"^\+?\d{1,4}[-.\s]?\d{9,15}$"

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise InvalidPhoneError("Phone value must be a string")
        if not re.match(self.__PHONE_REGEX, value):
            raise InvalidPhoneError(f"Invalid phone number {value}")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Phone):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value
