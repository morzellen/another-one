from enum import StrEnum


class BookingPaymentStatusesEnum(StrEnum):
    """
    This class represents the different payment statuses for booking transactions in the system.
    These statuses indicate whether payments have been processed or are pending.

    The fields in this class are:
    - PENDING: The payment is pending.
    - PAID: The payment has been processed.
    - REFUNDED: The payment has been refunded.
    - FAILED: The payment attempt has failed.
    """

    PENDING = "pending"  # Ожидает оплаты
    PAID = "paid"  # Оплачен
    REFUNDED = "refunded"  # Возвращён
    FAILED = "failed"  # Неудачная попытка оплаты


class BookingPaymentMethodsEnum(StrEnum):
    """
    This class represents the different payment methods available for booking transactions in the system.
    These methods allow clients to pay for studio services using various options.

    The fields in this class are:
    - CASH: The payment will be made in cash at the studio.
    - CARD: The payment will be made using a credit card.
    - ONLINE: The payment will be processed online using a payment gateway.
    """

    CASH = "cash"  # Наличные на студии
    CARD = "card"  # Банковская карта
    ONLINE = "online"  # Онлайн-платежи (ЮKassa и другие)
