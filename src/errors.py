class InvalidEmailError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class InvalidPhoneError(Exception):
    pass


class InvalidFileFormatError(Exception):
    pass


class InvalidBookingTimeRangeError(Exception):
    pass


class TrialLimitExceededError(Exception):
    """Исключение, возникающее при превышении лимита пробных периодов для владельца."""

    pass


class InvalidContactInfoError(Exception):
    pass


class InvalidEmployeeInfoError(Exception):
    pass


class InvalidPersonalInfoError(Exception):
    pass


class InvalidDiscountPolicyError(Exception):
    pass


class InvalidStudioConfigurationError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class PaymentFailedError(Exception):
    pass


class RoleAssignmentError(Exception):
    pass


class BookingCannotBeCompletedError(Exception):
    pass


class BookingCannotBeConfirmedError(Exception):
    pass


class BookingCannotBeCanceledError(Exception):
    pass


class BookingCannotBeRescheduledError(Exception):
    pass


class UnsupportedBookingServiceError(Exception):
    pass
