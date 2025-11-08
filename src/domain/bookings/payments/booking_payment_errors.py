class BookingPaymentRefundError(Exception):
    pass


class BookingPaymentAlreadyPaidError(Exception):
    pass


class InvalidBookingPaymentAmountError(Exception):
    pass
