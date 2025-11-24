from enum import StrEnum, auto, unique


@unique
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

    PENDING = auto()  # Ожидает оплаты
    PAID = auto()  # Оплачен
    REFUNDED = auto()  # Возвращён
    FAILED = auto()  # Неудачная попытка оплаты


@unique
class BookingPaymentMethodsEnum(StrEnum):
    """
    This class represents the different payment methods available for booking transactions in the system.
    These methods allow clients to pay for studio services using various options.

    The fields in this class are:
    - CASH: The payment will be made in cash at the studio.
    - CARD: The payment will be made using a credit card.
    """

    CASH = auto()  # Наличные на студии
    CARD = auto()  # Банковская карта


@unique
class BookingPaymentFormEnum(StrEnum):
    """ """

    ONLINE = auto()  # Всё, кроме наличных
    OFFLINE = auto()  # Всё в целом


class BookingPaymentCurrenciesEnum(StrEnum):
    RUB = auto()  # Российский рубль
    USD = auto()  # Доллар США
    EUR = auto()  # Евро
