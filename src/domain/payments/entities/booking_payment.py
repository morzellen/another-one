from datetime import datetime
from decimal import Decimal
from uuid import UUID
from dataclasses import dataclass

from ..enums.booking_payment_enum import BookingPaymentMethodsEnum, BookingPaymentStatusesEnum


@dataclass
class Payment:
    """
    Агрегат платежа, связанный с бронированием.

    Отвечает за управление статусом оплаты и обработку возвратов.
    Связь с бронированием осуществляется через booking_id (слабая связь).

    Бизнес-правила:
    - Оплата может быть только в статусе PENDING
    - Возврат возможен только для оплаченных платежей
    - При возврате статус меняется на REFUNDED
    """

    id: UUID
    booking_id: UUID  # Связь с агрегатом Booking через ID
    amount: Decimal  # Сумма платежа
    currency: str  # Валюта (ISO код: USD, EUR, RUB) TODO: реализовать через enum
    payment_method: BookingPaymentMethodsEnum = BookingPaymentMethodsEnum.ONLINE
    status: BookingPaymentStatusesEnum = BookingPaymentStatusesEnum.PENDING
    created_at: datetime = None
    paid_at: datetime | None = None
    refunded_at: datetime | None = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.amount <= 0:
            raise ValueError("Сумма платежа должна быть положительной")

    def mark_as_paid(self, paid_at: datetime):
        """Подтверждает получение оплаты"""
        if self.status != BookingPaymentStatusesEnum.PENDING:
            raise ValueError("Можно оплатить только платежи в статусе PENDING")
        self.status = BookingPaymentStatusesEnum.PAID
        self.paid_at = paid_at

    def refund(self, refunded_at: datetime):
        """Выполняет возврат средств"""
        if self.status != BookingPaymentStatusesEnum.PAID:
            raise ValueError("Можно вернуть деньги только за оплаченные платежи")
        self.status = BookingPaymentStatusesEnum.REFUNDED
        self.refunded_at = refunded_at
