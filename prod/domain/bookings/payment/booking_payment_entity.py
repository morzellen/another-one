from datetime import datetime
from decimal import Decimal
from uuid import UUID

import logging

from .booking_payment_events import (
    DomainEvent,
    BookingPaymentPaidEvent,
    BookingPaymentFailedEvent,
    BookingPaymentRefundedEvent,
)

from .booking_payment_errors import (
    BookingPaymentAlreadyPaidError,
    BookingPaymentFailedError,
    BookingPaymentRefundError,
    InvalidBookingPaymentAmountError,
)
from .booking_payment_enums import (
    BookingPaymentFormEnum,
    BookingPaymentMethodsEnum,
    BookingPaymentStatusesEnum,
    BookingPaymentCurrenciesEnum,
)

logger = logging.getLogger(__name__)


class BookingPayment:
    """
    Агрегат платежа для бронирования.
    """

    # region Constructor
    def __init__(
        self,
        id: UUID,
        amount: Decimal,
        currency: BookingPaymentCurrenciesEnum,
        payment_form: BookingPaymentFormEnum,
        payment_method: BookingPaymentMethodsEnum,
        created_at: datetime,
        paid_at: datetime | None = None,
        refunded_at: datetime | None = None,
        failed_at: datetime | None = None,
        status: BookingPaymentStatusesEnum = BookingPaymentStatusesEnum.PENDING,
    ):
        self._validate_amount(amount)
        self._id = id
        self._amount = amount
        self._currency = currency
        self._payment_form = payment_form
        self._payment_method = payment_method
        self._created_at = created_at
        self._paid_at = paid_at
        self._refunded_at = refunded_at
        self._failed_at = failed_at
        self._status = status

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
    def payment_form(self) -> BookingPaymentFormEnum:
        return self._payment_form

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

    @property
    def failed_at(self) -> datetime | None:
        return self._failed_at

    @property
    def is_pending(self) -> bool:
        return self._status == BookingPaymentStatusesEnum.PENDING

    @property
    def is_paid(self) -> bool:
        return self._paid_at is not None and self._status == BookingPaymentStatusesEnum.PAID

    @property
    def is_refunded(self) -> bool:
        return self._refunded_at is not None and self._status == BookingPaymentStatusesEnum.REFUNDED

    @property
    def is_failed(self) -> bool:
        return self._failed_at is not None and self._status == BookingPaymentStatusesEnum.FAILED

    @property
    def can_be_paid(self) -> bool:
        return self.is_pending and not self.is_paid

    @property
    def can_be_refunded(self) -> bool:
        return self.is_paid and not self.is_refunded

    @property
    def can_be_failed(self) -> bool:
        return self.is_pending

    # endregion

    # region Methods

    def mark_as_paid(self, current_time: datetime) -> list[DomainEvent]:
        """
        Отмечает платеж как успешно оплаченный и возвращает события.
        """
        if not self.can_be_paid:
            raise BookingPaymentAlreadyPaidError(self._status.value)

        self._status = BookingPaymentStatusesEnum.PAID
        self._paid_at = current_time

        event = BookingPaymentPaidEvent(
            occurred_at=self._paid_at,
            payment_id=self.id,
            amount=self.amount,
        )

        logger.info(f"📤 Публикация события успешной оплаты бронирования: {event.payment_id}")

        return [event]

    def mark_as_failed(self, current_time: datetime) -> list[DomainEvent]:
        """
        Отмечает платеж как неудачный и возвращает события.
        """
        if not self.can_be_failed:
            raise BookingPaymentFailedError(self._status.value)

        self._status = BookingPaymentStatusesEnum.FAILED
        self._failed_at = current_time

        event = BookingPaymentFailedEvent(
            occurred_at=self._failed_at,
            payment_id=self.id,
            amount=self.amount,
        )

        logger.info(f"📤 Публикация события неудачной оплаты бронирования: {event.payment_id}")

        return [event]

    def mark_as_refunded(
        self, current_time: datetime, refunded_reason: str | None = None
    ) -> list[DomainEvent]:
        """
        Отмечает платеж как возвращенный и возвращает события.
        """
        if not self.can_be_refunded:
            raise BookingPaymentRefundError(self._status.value)

        self._status = BookingPaymentStatusesEnum.REFUNDED
        self._refunded_at = current_time

        event = BookingPaymentRefundedEvent(
            occurred_at=self._refunded_at,
            payment_id=self.id,
            amount=self.amount,
            reason=refunded_reason,
        )

        logger.info(f"📤 Публикация события возврата платежа бронирования: {event.payment_id}")

        return [event]

    # endregion
