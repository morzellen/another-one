from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .booking_payment_errors import (
    BookingPaymentAlreadyPaidError,
    BookingPaymentRefundError,
    InvalidBookingPaymentAmountError,
)
from .booking_payment_enum import (
    BookingPaymentFormEnum,
    BookingPaymentMethodsEnum,
    BookingPaymentStatusesEnum,
    BookingPaymentCurrenciesEnum,
)


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
        currency: BookingPaymentCurrenciesEnum,
        created_at: datetime,
        status: BookingPaymentStatusesEnum = BookingPaymentStatusesEnum.PENDING,
        payment_form: BookingPaymentFormEnum | None = None,
        payment_method: BookingPaymentMethodsEnum | None = None,
        paid_at: datetime | None = None,
        refunded_at: datetime | None = None,
    ):
        self._validate_amount(amount)
        self._id = id
        self._booking_id = booking_id
        self._amount = amount
        self._currency = currency
        self._created_at = created_at
        self._status = status
        self._payment_form = payment_form
        self._payment_method = payment_method
        self._paid_at = paid_at
        self._refunded_at = refunded_at

    def _validate_amount(self, amount: Decimal) -> None:
        if amount <= 0:
            raise InvalidBookingPaymentAmountError(
                InvalidBookingPaymentAmountError.POSITIVE_MESSAGE, amount
            )
        if round(amount, 2) != amount:
            raise InvalidBookingPaymentAmountError(
                InvalidBookingPaymentAmountError.PRECISION_MESSAGE, amount
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
    def currency(self) -> BookingPaymentCurrenciesEnum:
        return self._currency

    @property
    def payment_form(self) -> BookingPaymentFormEnum | None:
        return self._payment_form

    @property
    def payment_method(self) -> BookingPaymentMethodsEnum | None:
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

    # region Methods

    def _update_payment_status(self, status: BookingPaymentStatusesEnum) -> None:
        """Обновляет статус оплаты."""
        self._status = status

    def mark_as_paid(self, paid_at: datetime) -> None:
        """Подтверждает получение оплаты"""
        if self._status != BookingPaymentStatusesEnum.PENDING:
            raise BookingPaymentAlreadyPaidError(status=self._status.value)
        self._update_payment_status(BookingPaymentStatusesEnum.PAID)
        self._paid_at = paid_at

    def refund(self, refunded_at: datetime) -> None:
        """Выполняет возврат средств"""
        if self._status != BookingPaymentStatusesEnum.PAID:
            raise BookingPaymentRefundError(
                BookingPaymentRefundError.INVALID_STATUS_MESSAGE, self._status.value
            )
        if self._paid_at and refunded_at < self._paid_at:
            raise BookingPaymentRefundError(BookingPaymentRefundError.INVALID_REFUND_DATE_MESSAGE)
        self._update_payment_status(BookingPaymentStatusesEnum.REFUNDED)
        self._refunded_at = refunded_at

    # endregion
