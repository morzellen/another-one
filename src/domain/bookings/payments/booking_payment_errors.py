from decimal import Decimal


class BookingPaymentRefundError(Exception):
    INVALID_STATUS_MESSAGE = (
        "Возврат возможен только для оплаченных платежей. Текущий статус: {status}"
    )
    INVALID_REFUND_DATE_MESSAGE = "Дата возврата не может быть раньше даты оплаты"

    def __init__(self, message_template: str, status: str = None):
        if status is not None:
            message = message_template.format(status=status)
        else:
            message = message_template
        super().__init__(message)


class BookingPaymentAlreadyPaidError(Exception):
    DEFAULT_MESSAGE = "Платёж в статусе {status} не может быть оплачен повторно"

    def __init__(self, status: str):
        super().__init__(self.DEFAULT_MESSAGE.format(status=status))


class InvalidBookingPaymentAmountError(Exception):
    DEFAULT_MESSAGE = "Неверная сумма платежа: {amount}."
    POSITIVE_MESSAGE = "Сумма платежа должна быть положительной. Текущая сумма: {amount}"
    PRECISION_MESSAGE = (
        "Сумма должна иметь не более 2 знаков после запятой. Текущая сумма: {amount}"
    )

    def __init__(self, message_template: str, amount: Decimal):
        message = message_template.format(amount=amount)
        super().__init__(message)
