from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ..errors import InvalidTimeRangeError
from ..value_objects.value_objects import DiscountPolicy


@dataclass
class Studio:
    """
    - Этот класс представляет студию звукозаписи на платформе управления студиями.
    - Студии являются центральными местами, где клиенты могут создавать проекты, покупать услуги и т.д.
    - Студиями управляют владельцы и имеют уникальный идентификатор (UUID).
    - Это основная часть SaaS-системы, где происходит вся активность.
    - Сначала создается студия (по желанию с начальной пробной подпиской),
    а затем к ней можно привязывать/обновлять подписки.
    - На студии завязаны работники, клиенты — в общем, пользователи.
    - У 1 студии может быть только 1 владелец.
    - У 1 владельца может быть несколько студий.
    """

    id: UUID
    owner_id: UUID  # link to User.id
    name: str
    created_at: datetime
    updated_at: datetime | None = None
    discount_policy: DiscountPolicy | None = None
    subscription_id: UUID | None = None

    _is_on_trial: bool = False
    _trial_expires_at: datetime | None = None

    def __post_init__(self):
        # Гарантируем, что если trial_expires_at установлен, то он в будущем.
        if self._trial_expires_at and self._trial_expires_at <= datetime.now():
            raise InvalidTimeRangeError("Trial expiration date must be in the future.")

    @property
    def is_on_trial(self) -> bool:
        """
        Возвращает текущий статус пробного периода студии.

        Сценарии использования:
        - Проверка в пользовательском интерфейсе, чтобы отобразить статус студии (например, "Пробный период активен").
        - Логика в сервисах для определения доступных функций (например, ограничение премиум-функций).
        - Анализ состояния студии в отчетах или аналитике.
        """
        return self._is_on_trial

    @property
    def trial_expires_at(self) -> datetime | None:
        """
        Возвращает дату истечения пробного периода.

        Сценарии использования:
        - Отображение оставшегося времени пробного периода в интерфейсе пользователя.
        - Проверка истечения в фоновых задачах (например, планировщике для автоматической деактивации).
        - Логика уведомлений владельца о скором окончании пробного периода.
        """
        return self._trial_expires_at

    def activate_trial_internal(self, expires_at: datetime):
        """
        Внутренний метод для активации пробного периода.
        Должен вызываться ТОЛЬКО из методов сущности, которые гарантируют инварианты.
        """
        if expires_at <= datetime.now():
            raise InvalidTimeRangeError("Trial expiration date must be in the future.")
        self._is_on_trial = True
        self._trial_expires_at = expires_at
        self.updated_at = datetime.now()

    def deactivate_trial_internal(self):
        """
        Внутренний метод для деактивации пробного периода.
        """
        self._is_on_trial = False
        self._trial_expires_at = None
        self.updated_at = datetime.now()

    def is_trial_active(self) -> bool:
        """
        Проверяет, активен ли пробный период.

        Сценарии использования:
        - Определение доступности функций студии в реальном времени (например, ограничение премиум-функций после истечения).
        - Логика уведомлений владельца о состоянии пробного периода.
        - Автоматическая деактивация пробного периода в фоновых задачах при истечении.
        """
        return self._is_on_trial and (
            self._trial_expires_at is None or self._trial_expires_at > datetime.now()
        )

    def has_subscription(self) -> bool:
        return self.subscription_id is not None

    def rename(self, new_name: str):
        """
        Изменяет название студии.
        """
        if not new_name or not new_name.strip():
            raise ValueError("Studio name cannot be empty")
        self.name = new_name.strip()
        self.updated_at = datetime.now()

    def update_discount_policy(self, new_policy: DiscountPolicy | None):
        """
        Обновляет политику скидок для студии.
        """
        # Если policy не None, проверяем, что она принадлежит этой студии
        if new_policy and new_policy.studio_id != self.id:
            raise ValueError("Discount policy must belong to this studio")
        self.discount_policy = new_policy
        self.updated_at = datetime.now()

    # set_description(desc: str)

    # set_logo_url(url: str)
