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
