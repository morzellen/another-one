from decimal import Decimal


class BookingPaymentRefundError(Exception):
    DEFAULT_MESSAGE = "Возврат возможен только для оплаченных платежей. Текущий статус: {status}"

    def __init__(self, status: str):
        super().__init__(self.DEFAULT_MESSAGE.format(status=status))


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


class BookingPaymentFailedError(Exception):
    DEFAULT_MESSAGE = "Невозможно отметить платеж как неудачный. Текущий статус: {status}"

    def __init__(self, status: str):
        super().__init__(self.DEFAULT_MESSAGE.format(status=status))
