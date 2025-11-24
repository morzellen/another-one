from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal

from .booking_order import BookingOrder
from .booking.booking_enums import BookingServicesTypesEnum, BookingPaymentCurrenciesEnum
from .booking.value_object.booking_time_range_vo import BookingTimeRange
from .booking import Booking
from .payment import BookingPayment
from .payment.booking_payment_enums import BookingPaymentFormEnum, BookingPaymentMethodsEnum


class BookingOrderFactory:
    """
    Фабрика для создания агрегата BookingOrder.
    Инкапсулирует бизнес-правила создания заказа бронирования.
    """

    @classmethod
    def create_booking_order(
        cls,
        studio_id: UUID,
        client_id: UUID,
        assigned_employee_id: UUID,
        service_type: BookingServicesTypesEnum,
        time_range: BookingTimeRange,
        amount: Decimal,
        currency: BookingPaymentCurrenciesEnum,
        payment_form: BookingPaymentFormEnum,
        payment_method: BookingPaymentMethodsEnum,
        project_id: UUID | None = None,
    ) -> BookingOrder:
        """
        Создает новый заказ бронирования.
        Генерирует ID для агрегата и всех внутренних сущностей.
        """
        current_time = datetime.now()

        # Генерируем ID для агрегата и его компонентов
        order_id = uuid4()
        booking_id = uuid4()
        payment_id = uuid4()

        # Создаем бронирование
        booking = Booking(
            id=booking_id,
            studio_id=studio_id,
            client_id=client_id,
            assigned_employee_id=assigned_employee_id,
            service_type=service_type,
            time_range=time_range,
            created_at=current_time,
            project_id=project_id,
        )

        # Создаем платеж
        payment = BookingPayment(
            id=payment_id,
            amount=amount,
            currency=currency,
            created_at=current_time,
            payment_form=payment_form,
            payment_method=payment_method,
        )

        # Создаем и возвращаем агрегат
        return BookingOrder(id=order_id, booking=booking, payment=payment)

    @classmethod
    def reconstruct_booking_order(
        cls, order_id: UUID, booking: Booking, payment: BookingPayment
    ) -> BookingOrder:
        """
        Восстанавливает агрегат из persistence.
        Используется в репозиториях при загрузке из базы.
        """
        return BookingOrder(id=order_id, booking=booking, payment=payment)
