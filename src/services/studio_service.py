from decimal import Decimal
from uuid import UUID
from datetime import datetime, timedelta

from ..enums import (
    PricingPlanEnum,
    SubscriptionStatusesEnum,
    UserRoleEnum,
    UserStatusesEnum,
)

from ..entities.studio import Studio
from ..entities.subscription import Subscription
from ..entities.user_studio_membership import UserStudioMembership
from ..repositories.studio_repository import StudioRepository
from ..repositories.subscription_repository import SubscriptionRepository
from ..errors import TrialLimitExceededError, InvalidTimeRangeError
from ..value_objects.value_objects import DiscountPolicy, TimeRange


class StudioService:
    def __init__(
        self,
        studio_repo: StudioRepository,
        subscription_repo: SubscriptionRepository,
        membership_repo: UserStudioMembershipRepository,
        trial_limit_service: TrialLimitService,
        payment_service: PaymentService,
    ):
        self.studio_repo = studio_repo
        self.subscription_repo = subscription_repo
        self.membership_repo = membership_repo
        self.trial_limit_service = trial_limit_service
        self.payment_service = payment_service

    def create_studio(
        self, owner_id: UUID, name: str, with_trial: bool = False
    ) -> Studio:
        """Создаёт новую студию."""
        studio = Studio(
            id=UUID(...),
            owner_id=owner_id,
            name=name,
            created_at=datetime.now(),
            is_on_trial=False,
            trial_expires_at=None,
        )
        self.studio_repo.save(studio)

        # Назначаем владельца
        membership = UserStudioMembership(
            user_id=owner_id,
            studio_id=studio.id,
            roles={UserRoleEnum.OWNER},
            joined_at=datetime.now(),
            status=UserStatusesEnum.ACTIVE,
        )
        self.membership_repo.save(membership)

        if with_trial:
            self.activate_trial(studio.id, days=14)

        return studio

    # days вынести в константы
    def activate_trial(self, studio_id: UUID, days: int = 14) -> Studio:
        """Активирует пробный период для студии."""
        studio = self.studio_repo.find_by_id(studio_id)
        if not studio:
            raise ValueError("Studio not found")
        if not self.trial_limit_service.can_activate_trial_for_owner(studio.owner_id):
            raise TrialLimitExceededError("Trial limit exceeded for owner")
        end_time = datetime.now() + timedelta(days=days)
        # Активируем пробный период через внутренний метод сущности
        studio.activate_trial_internal(end_time)
        # Создаём запись в аудите
        # (здесь можно добавить вызов AuditService)
        self.studio_repo.save(studio)
        return studio

    # вынести в константы
    def get_pricing_for_plan(self, plan: PricingPlanEnum) -> Decimal:
        """Возвращает цену для плана подписки."""
        prices = {
            PricingPlanEnum.BASIC: Decimal("9.99"),
            PricingPlanEnum.PRO: Decimal("29.99"),
            PricingPlanEnum.TRIAL: Decimal("0.00"),
        }
        return prices.get(plan, Decimal("0.00"))

    def renew_subscription(self, studio_id: UUID, plan: str) -> Subscription:
        """Продлевает подписку для студии."""
        studio = self.studio_repo.find_by_id(studio_id)
        if not studio:
            raise ValueError("Studio not found")

        pricing_plan = PricingPlanEnum(plan)
        price = self.get_pricing_for_plan(pricing_plan)  # Выносим в отдельный метод
        # Создаём новую подписку
        subscription = Subscription(
            id=UUID(...),
            studio_id=studio.id,
            pricing_plan=pricing_plan,
            period=TimeRange(start_time=datetime.now(), end_time=None),  # Бессрочная
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status=SubscriptionStatusesEnum.PENDING,
        )
        self.subscription_repo.save(subscription)
        # Обновляем студию
        studio.subscription_id = subscription.id
        self.studio_repo.save(studio)
        # Обрабатываем оплату
        self.payment_service.process_payment(subscription.id, price)
        return subscription

    def get_studio_by_name(self, name: str) -> Studio | None:
        """Находит студию по имени."""
        return self.studio_repo.find_by_name(name)

    def get_studios_for_user(self, user_id: UUID) -> list[Studio]:
        """Возвращает список студий, где пользователь имеет доступ."""
        memberships = self.membership_repo.find_by_user(user_id)
        studios = []
        for membership in memberships:
            if membership.is_active():
                studio = self.studio_repo.find_by_id(membership.studio_id)
                if studio:
                    studios.append(studio)
        return studios

    def configure_studio(self, studio_id: UUID, config: dict) -> Studio:
        """
        Настраивает студию.
        - Если config содержит необязательные поля, то сервис должен их игнорировать, если они не указаны.
        """
        studio = self.studio_repo.find_by_id(studio_id)
        if not studio:
            raise ValueError("Studio not found")

        # Обрабатываем каждое поле конфигурации отдельно
        if "name" in config:
            studio.rename(config["name"])

        if "discount_policy" in config:
            # Предполагаем, что discount_policy передаётся как объект DiscountPolicy
            # Если передаётся словарь, нужно сначала создать VO
            studio.update_discount_policy(config["discount_policy"])

        # Можно добавить другие поля по аналогии
        # if "description" in config:
        #     studio.set_description(config["description"])

        self.studio_repo.save(studio)
        return studio
