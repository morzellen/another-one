from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .booking_payment_errors import (
    BookingPaymentAlreadyPaidError,
    BookingPaymentRefundError,
    InvalidBookingPaymentAmountError,
)
from .booking_payment_enum import BookingPaymentMethodsEnum, BookingPaymentStatusesEnum


class BookingPayment:
    """
    Агрегат платежа для бронирования.
    """

    # region Constructor
    def __init__(
        self,
        id: UUID,
        booking_id: UUID,
        amount: Decimal,
        currency: str,  # TODO: need to add enum
        created_at: datetime,
        status: BookingPaymentStatusesEnum = BookingPaymentStatusesEnum.PENDING,
        payment_method: BookingPaymentMethodsEnum = BookingPaymentMethodsEnum.CASH,
        paid_at: datetime | None = None,
        refunded_at: datetime | None = None,
    ):
        self._validate_amount(amount)
        self._id = id
        self._booking_id = booking_id
        self._amount = amount
        self._currency = currency.upper()
        self._created_at = created_at
        self._status = status
        self._payment_method = payment_method
        self._paid_at = paid_at
        self._refunded_at = refunded_at

    # TODO: check this method cause we change amount from float to Decimal
    # строковое представление ошибки вынести куда-то
    def _validate_amount(self, amount: Decimal) -> None:
        if amount <= 0:
            raise InvalidBookingPaymentAmountError("Сумма платежа должна быть положительной")
        if round(amount, 2) != amount:
            raise InvalidBookingPaymentAmountError(
                "Сумма должна иметь не более 2 знаков после запятой"
            )

    # endregion

    # region Properties
    @property
    def id(self) -> UUID:
        return self._id

    @property
    def booking_id(self) -> UUID:
        return self._booking_id

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def payment_method(self) -> BookingPaymentMethodsEnum:
        return self._payment_method

    @property
    def status(self) -> BookingPaymentStatusesEnum:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def paid_at(self) -> datetime | None:
        return self._paid_at

    @property
    def refunded_at(self) -> datetime | None:
        return self._refunded_at

    # endregion

    # region Methods TODO: вынести комментарии к ошибкам в какие-то константы (возможно засунуть в классы этих ошибок)
    def mark_as_paid(self, paid_at: datetime) -> None:
        """Подтверждает получение оплаты"""
        if self._status != BookingPaymentStatusesEnum.PENDING:
            raise BookingPaymentAlreadyPaidError(
                f"Платёж в статусе {self._status.value} не может быть оплачен повторно"
            )
        self._status = BookingPaymentStatusesEnum.PAID
        self._paid_at = paid_at

    def refund(self, refunded_at: datetime) -> None:
        """Выполняет возврат средств"""
        if self._status != BookingPaymentStatusesEnum.PAID:
            raise BookingPaymentRefundError(
                f"Возврат возможен только для оплаченных платежей. Текущий статус: {self._status.value}"
            )
        self._status = BookingPaymentStatusesEnum.REFUNDED
        self._refunded_at = refunded_at

    # TODO: подумать, надо ли оно нам здесь
    def update_payment_status(self, payment_status: BookingPaymentStatusesEnum):
        """Обновляет статус оплаты."""
        self._payment_status = payment_status

    # endregion
