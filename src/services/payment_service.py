# src/services/payment_service.py

from decimal import Decimal
from uuid import UUID

from ..entities.subscription import Subscription
from ..repositories.subscription_repository import SubscriptionRepository
from ..errors import PaymentFailedError


class PaymentService:
    def __init__(self, subscription_repo: SubscriptionRepository):
        self.subscription_repo = subscription_repo

    def process_payment(self, subscription_id: UUID, amount: Decimal) -> bool:
        """Обрабатывает оплату подписки."""
        subscription = self.subscription_repo.find_by_id(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")

        # Интеграция с платежной системой
        payment_success = self._call_payment_gateway(subscription, amount)

        if payment_success:
            subscription.activate(payment_id=UUID(...))  # Генерируем ID платежа
            self.subscription_repo.save(subscription)
            return True
        else:
            subscription.expire()
            self.subscription_repo.save(subscription)
            raise PaymentFailedError("Payment failed")

    def _call_payment_gateway(
        self, subscription: Subscription, amount: Decimal
    ) -> bool:
        """Вызов внешнего API платежной системы."""
        # Реализация зависит от шлюза
        # Пример: Stripe, PayPal, YooKassa
        return True  # Заглушка
