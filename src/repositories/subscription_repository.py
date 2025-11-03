from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from ..entities.subscription import Subscription


class SubscriptionRepository(ABC):
    @abstractmethod
    def find_by_id(self, subscription_id: UUID) -> Optional[Subscription]:
        pass

    @abstractmethod
    def save(self, subscription: Subscription):
        pass


class InMemorySubscriptionRepository(SubscriptionRepository):
    def __init__(self):
        self.subscriptions = {}

    def find_by_id(self, subscription_id: UUID) -> Optional[Subscription]:
        return self.subscriptions.get(subscription_id)

    def save(self, subscription: Subscription):
        self.subscriptions[subscription.id] = subscription
