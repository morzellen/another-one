from uuid import UUID
from datetime import datetime

from .booking.booking_entity import Booking
from .payment.booking_payment_entity import BookingPayment


class BookingOrder:
    """
    Агрегат заказа бронирования, содержащий бронирование и платеж.
    Корневой агрегат, обеспечивающий целостность данных.
    """

    def __init__(self, id: UUID, booking: Booking, payment: BookingPayment):
        self._id = id
        self._booking = booking
        self._payment = payment
        self._ensure_consistency()

    def _ensure_consistency(self) -> None:
        """Проверяет целостность агрегата"""
        # Можно добавить проверки, например, что валюта платежа соответствует студии и т.д.
        pass

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def booking(self) -> Booking:
        return self._booking

    @property
    def payment(self) -> BookingPayment:
        return self._payment

    # Делегируем основные методы бронированию
    def confirm(self, current_time: datetime):
        event = self._booking.mark_as_confirm(current_time)
        # Здесь можно добавить логику, связанную с платежом при подтверждении
        return event

    # Бизнес-правило: отмена заказа должна включать попытку возврата
    def cancel_with_refund(self, current_time: datetime, reason: str) -> List[DomainEvent]:
        # 1. Отменяем бронирование (обязательно)
        booking_events = self._booking.mark_as_cancelled(current_time, reason)

        # 2. Пытаемся вернуть платеж (часть бизнес-процесса)
        try:
            refund_events = self._payment.mark_as_refunded(
                current_time, f"Автоматический возврат: {reason}"
            )
            return booking_events + refund_events
        except BookingPaymentRefundError:
            logger.warning(f"Возврат невозможен для заказа {self.id}, но отмена выполнена")
            return booking_events
