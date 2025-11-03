# File: src/console_app.py
"""
Консольное приложение для тестирования основных сценариев системы.
Реализует логику, описанную в блок-схеме: вход/регистрация, создание студии, управление подпиской.
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from .entities.auth_identity import AuthIdentity
from .enums import AuthProviderEnum
from .constants import UserRoleEnum, PricingPlanEnum
from .entities.user import User
from .entities.studio import Studio
from .entities.subscription import Subscription
from .entities.user_studio_membership import UserStudioMembership
from .services.authentication_service import AuthenticationService
from .services.studio_service import StudioService
from .services.subscription_service import SubscriptionService
from .services.user_service import UserService
from .services.authorization_service import AuthorizationService
from .services.payment_service import PaymentService
from .services.trial_limit_service import TrialLimitService
from .value_objects.value_objects import (
    ContactInfo,
    Email,
    PersonalInfo,
    TimeRange,
    StudioConfiguration,
)
from src.repositories.studio_repository import InMemoryStudioRepository
from src.repositories.subscription_repository import InMemorySubscriptionRepository
from src.repositories.user_studio_membership_repository import (
    InMemoryUserStudioMembershipRepository,
)
from src.ui.console_ui import ConsoleUI  # Импортируем новый UI-модуль


# In-memory repositories for testing
class InMemoryUserRepository:
    def __init__(self):
        self.users = {}

    def find_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self.users.get(user_id)

    def find_by_email(self, email: Email) -> Optional[User]:
        for user in self.users.values():
            if user.contact_info.email == email:
                return user
        return None

    def find_by_provider_id(
        self, provider: str, provider_user_id: str
    ) -> Optional[User]:
        # В тестовом режиме просто возвращаем None
        return None

    def save(self, user: User):
        # NOTE: Проверка уникальности email теперь должна быть в UserService.register_user
        # Убираем её отсюда, чтобы не нарушать архитектуру.
        # if user.contact_info.email:
        #     existing_user = self.find_by_email(user.contact_info.email)
        #     if existing_user and existing_user.id != user.id:
        #         raise ValueError(f"User with email {user.contact_info.email.value} already exists.")
        self.users[user.id] = user


class InMemoryAuthIdentityRepository:
    def __init__(self):
        self.identities = {}

    def find_by_user_and_provider(
        self, user_id: uuid.UUID, provider: AuthProviderEnum
    ) -> Optional[AuthIdentity]:
        return self.identities.get((user_id, provider))

    def save(self, identity: AuthIdentity):
        self.identities[(identity.user_id, identity.provider)] = identity


class InMemoryAuditRepository:
    def __init__(self):
        self.audits = []

    def save(self, audit: object):
        self.audits.append(audit)


class InMemorySessionRepository:
    def __init__(self):
        self.sessions = {}

    def save(self, session_id: str, user_id: uuid.UUID, created_at: datetime):
        self.sessions[session_id] = {"user_id": user_id, "created_at": created_at}

    def delete(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]


class ConsoleApp:
    """Основной класс консольного приложения для тестирования."""

    def __init__(self):
        # Инициализируем все необходимые сервисы с in-memory репозиториями
        self.user_repo = InMemoryUserRepository()
        self.auth_identity_repo = InMemoryAuthIdentityRepository()
        self.studio_repo = InMemoryStudioRepository()
        self.subscription_repo = InMemorySubscriptionRepository()
        self.membership_repo = InMemoryUserStudioMembershipRepository()
        self.audit_repo = InMemoryAuditRepository()
        self.session_repo = InMemorySessionRepository()

        # Создаем сервисы
        self.auth_service = AuthenticationService(
            user_repo=self.user_repo, auth_identity_repo=self.auth_identity_repo
        )
        self.user_service = UserService(
            user_repo=self.user_repo,
            auth_identity_repo=self.auth_identity_repo,
            membership_repo=self.membership_repo,
        )

        # Создаём SubscriptionService
        self.subscription_service = SubscriptionService(
            subscription_repo=self.subscription_repo,
            studio_repo=self.studio_repo,
            trial_limit_service=TrialLimitService(self.studio_repo),
            payment_service=PaymentService(self.subscription_repo),
        )

        # Передаём SubscriptionService в StudioService
        self.studio_service = StudioService(
            studio_repo=self.studio_repo,
            membership_repo=self.membership_repo,
            subscription_service=self.subscription_service,
        )

        self.authorization_service = AuthorizationService(self.membership_repo)

        # Текущий пользователь и студия
        self.current_user: Optional[User] = None
        self.current_studio: Optional[Studio] = None

    def run(self):
        """Запуск консольного приложения."""
        while True:
            if not self.current_user:
                self.show_landing_page()
            else:
                # ВСЕГДА определяем роль и показываем соответствующее меню
                self.check_user_role()

    def show_landing_page(self):
        """Показывает главную страницу продукта."""
        ConsoleUI.display_welcome()
        choice = ConsoleUI.get_main_action()
        if choice == "1":
            self.login()
        elif choice == "2":
            self.register()
        elif choice == "3":
            print("Выход из программы...")
            exit(0)
        else:
            ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")

    def login(self):
        """Процесс входа пользователя."""
        choice = ConsoleUI.get_login_method()
        if choice == "1":
            self.native_login()
        elif choice == "2":
            self.oauth2_login()
        elif choice == "3":
            return
        else:
            ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")

    def native_login(self):
        """Вход по нативному логину/паролю."""
        email, password = ConsoleUI.get_native_login_credentials()
        try:
            user = self.auth_service.authenticate_native(email, password)
            self.current_user = user
            ConsoleUI.display_success("Успешный вход!")
            # Проверяем роль пользователя
            self.check_user_role()
        except Exception as e:
            ConsoleUI.display_error(f"Ошибка входа: {e}")

    def oauth2_login(self):
        """Вход через OAuth2."""
        provider, token = ConsoleUI.get_oauth2_login_credentials()
        try:
            user = self.auth_service.authenticate_oauth2(provider, token)
            self.current_user = user
            ConsoleUI.display_success(
                f"Успешный вход через OAuth2! Привет, {user.personal_info.first_name or 'Пользователь'}!"
            )
            # Проверяем роль пользователя
            self.check_user_role()
        except Exception as e:
            ConsoleUI.display_error(f"Ошибка входа через OAuth2: {e}")

    def register(self):
        """Регистрация нового пользователя."""
        email, password = ConsoleUI.get_registration_credentials()
        try:
            # Проверка уникальности email теперь находится в UserService.register_user
            user = self.user_service.register_user(email, password)
            self.current_user = user
            ConsoleUI.display_success(f"Регистрация успешна!")
            # После регистрации — сразу в личный кабинет ПП
            self.show_potential_buyer_menu()
        except Exception as e:
            ConsoleUI.display_error(f"Ошибка регистрации: {e}")

    def check_user_role(self):
        """Проверяет роль пользователя и перенаправляет в соответствующий интерфейс."""
        # Получаем все студии, где пользователь имеет доступ
        studios = self.studio_service.get_studios_for_user(self.current_user.id)
        is_owner = False
        is_potential_buyer = False

        if not studios:
            # Пользователь не связан ни с одной студией - он потенциальный покупатель
            is_potential_buyer = True
        else:
            # Проверяем, является ли пользователь владельцем хотя бы одной студии
            for studio in studios:
                membership = self.membership_repo.find_by_user_and_studio(
                    self.current_user.id, studio.id
                )
                if membership and UserRoleEnum.OWNER in membership.roles:
                    is_owner = True
                    break

        # Отображаем информацию о роли
        if is_owner:
            print(f"Вы вошли как Владелец. У вас {len(studios)} студий.")
        elif is_potential_buyer:
            print("Вы вошли как Потенциальный покупатель.")
        else:
            print(f"Вы вошли как Клиент или Сотрудник. У вас {len(studios)} студий.")

        # Запрашиваем действие в зависимости от роли
        choice = ConsoleUI.get_user_action_for_role(is_owner, is_potential_buyer)
        if is_owner:
            if choice == "1":
                self.select_studio()
            elif choice == "2":
                self.show_owner_menu()
            elif choice == "3":
                self.logout()
            else:
                ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")
        elif is_potential_buyer:
            if choice == "1":
                self.show_potential_buyer_menu()
            elif choice == "2":
                self.logout()
            else:
                ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")
        else:  # клиент или сотрудник
            if choice == "1":
                self.select_studio()
            elif choice == "2":
                self.logout()
            else:
                ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")

    def show_potential_buyer_menu(self):
        """Меню для потенциального покупателя."""
        choice = ConsoleUI.get_potential_buyer_action()
        if choice == "1":
            # Возврат к выбору действия на главной странице (в check_user_role)
            return
        elif choice == "2":
            self.create_studio_flow()
        elif choice == "3":
            self.update_personal_info()
        else:
            ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")

    def create_studio_flow(self):
        """Процесс создания студии для потенциального покупателя."""
        ConsoleUI.display_info(
            "Вы можете создать свою студию. При первом создании автоматически активируется пробный период (TRIAL) на 14 дней."
        )

        try:
            name = ConsoleUI.get_studio_creation_data()  # Игнорируем with_trial

            # 0. Проверим, не исчерпан ли лимит триалов (логика в StudioService.create_studio)
            can_trial = self.studio_service.subscription_service.trial_limit_service.can_activate_trial_for_owner(
                self.current_user.id
            )
            if not can_trial:
                ConsoleUI.display_warning(
                    "Вы уже использовали пробный период. Студия будет создана без TRIAL."
                )

            # 1. Создаём студию. Пробный период активируется автоматически, если лимит позволяет.
            studio = self.studio_service.create_studio(
                owner_id=self.current_user.id,
                name=name,
                with_trial=can_trial,  # <-- Передаём результат проверки
            )

            # Загружаем связанную подписку для отображения
            subscription = None
            if studio.subscription_id:
                subscription = self.subscription_repo.find_by_id(studio.subscription_id)

            # 2. Настраиваем конфигурацию
            config_data = {}
            description = (
                input("Введите описание студии (опционально): ").strip() or None
            )
            logo_url = input("Введите URL логотипа (опционально): ").strip() or None
            if description:
                config_data["description"] = description
            if logo_url:
                config_data["logo_url"] = logo_url
            if config_data:
                self.studio_service.configure_studio(
                    studio.id, config_data
                )  # Передаём словарь в сервис
                # self.studio_repo.save(studio) # configure_studio уже сохраняет

            ConsoleUI.display_studio_created_success(studio, subscription)
            self.current_studio = studio
            # Переходим в меню владельца
            ConsoleUI.wait_for_enter()
            # ВАЖНО: После создания студии пользователь становится владельцем. Нужно обновить состояние.
            # self.check_user_role() # Это вызовет лишний раз check_user_role, лучше сразу перейти.
            self.show_owner_menu()  # Пользователь теперь владелец, показываем его меню.
        except Exception as e:
            ConsoleUI.display_error(f"Ошибка создания студии: {e}")

    def show_owner_menu(self):
        """Меню для владельца студии."""
        choice = ConsoleUI.get_owner_action()
        if choice == "1":
            self.select_studio()
        elif choice == "2":
            self.show_owner_dashboard()
        elif choice == "3":
            self.logout()
        else:
            ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")

    def show_owner_dashboard(self):
        """Личный кабинет владельца."""
        choice = ConsoleUI.get_owner_dashboard_action()
        if choice == "1":
            # Возвращаемся в меню владельца или проверяем роль заново, если пользователь может быть и ПП и Владельцем
            # self.check_user_role() # Это может быть избыточно
            self.show_owner_menu()  # Проще вернуться в меню владельца
            return
        elif choice == "2":
            self.renew_subscription()
        elif choice == "3":
            self.update_personal_info()
        else:
            ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")

    def show_client_or_employee_menu(self):
        """Меню для клиента или сотрудника."""
        choice = ConsoleUI.get_client_or_employee_action()
        if choice == "1":
            self.select_studio()
        elif choice == "2":
            self.logout()
        else:
            ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")

    def select_studio(self):
        """Выбор студии из доступных."""
        studios = self.studio_service.get_studios_for_user(self.current_user.id)
        selected_studio = ConsoleUI.select_studio(studios)
        if selected_studio:
            self.current_studio = selected_studio
            self.show_studio_menu()

    def show_studio_menu(self):
        """Меню для выбранной студии."""
        if not self.current_studio:
            # Если студия не выбрана, возвращаемся к меню владельца
            self.show_owner_menu()
            return

        # Получаем роли пользователя в этой студии
        membership = self.membership_repo.find_by_user_and_studio(
            self.current_user.id, self.current_studio.id
        )
        if not membership:
            ConsoleUI.display_error("Ошибка: Вы не имеете доступа к этой студии.")
            # Возвращаемся к выбору студии
            self.select_studio()
            return
        roles = list(membership.roles)

        # Отображаем функционал в зависимости от ролей
        functionality = self.authorization_service.get_user_functionality_in_studio(
            self.current_user.id, self.current_studio.id
        )

        # Загружаем связанную подписку для отображения
        subscription = None
        if self.current_studio.subscription_id:
            subscription = self.subscription_repo.find_by_id(
                self.current_studio.subscription_id
            )

        ConsoleUI.display_studio_menu(
            self.current_studio, roles, functionality, subscription
        )
        choice = ConsoleUI.get_studio_management_action()
        if choice == "1":
            self.current_studio = None
            self.show_owner_menu()  # Возвращаемся в меню владельца
            return
        elif choice == "2":
            self.configure_studio()
        elif choice == "3":
            self.manage_subscription()
        elif choice == "4":
            self.show_studio_info()
        else:
            ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")

    def configure_studio(self):
        """Настройка студии."""
        if not self.current_studio:
            ConsoleUI.display_error("Не выбрана студия.")
            self.show_studio_menu()  # Возвращаемся в меню студии
            return
        choice = ConsoleUI.get_configure_studio_action()
        if choice == "1":
            try:
                new_name = ConsoleUI.get_new_studio_name()
                self.studio_service.configure_studio(
                    self.current_studio.id, {"name": new_name}
                )
                ConsoleUI.display_success("Название студии успешно изменено.")
            except Exception as e:
                ConsoleUI.display_error(f"Ошибка изменения названия: {e}")
        elif choice == "2":
            try:
                description = ConsoleUI.get_new_studio_description()
                # Передаём словарь с конфигурацией
                config = {"description": description}
                self.studio_service.configure_studio(self.current_studio.id, config)
                ConsoleUI.display_success("Описание студии успешно обновлено.")
            except Exception as e:
                ConsoleUI.display_error(f"Ошибка обновления описания: {e}")
        elif choice == "3":
            try:
                logo_url = ConsoleUI.get_new_studio_logo_url()
                self.studio_service.configure_studio(
                    self.current_studio.id, {"logo_url": logo_url}
                )
                ConsoleUI.display_success("Логотип студии успешно обновлен.")
            except Exception as e:
                ConsoleUI.display_error(f"Ошибка обновления логотипа: {e}")
        elif choice == "4":
            ConsoleUI.display_info(
                "Политика скидок пока не реализована в этом тестовом приложении."
            )
        elif choice == "5":
            self.show_studio_menu()  # Возвращаемся в меню студии
            return
        else:
            ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")

    def manage_subscription(self):
        """Управление подпиской студии."""
        if not self.current_studio:
            ConsoleUI.display_error("Не выбрана студия.")
            self.show_studio_menu()  # Возвращаемся в меню студии
            return
        choice = ConsoleUI.get_subscription_management_action()
        if choice == "1":
            self.show_studio_menu()  # Возвращаемся в меню студии
            return
        elif choice == "2":
            self.renew_subscription()
        elif choice == "3":
            ConsoleUI.display_pricing()
        else:
            ConsoleUI.display_error("Неверный выбор. Попробуйте снова.")

    def renew_subscription(self):
        """Продление подписки."""
        if not self.current_studio:
            ConsoleUI.display_error("Не выбрана студия.")
            return
        try:
            plan = ConsoleUI.get_pricing_plan()
            subscription = self.subscription_service.renew_subscription(
                self.current_studio.id, plan
            )
            ConsoleUI.display_success(
                f"Подписка успешно продлена! Новый план: {subscription.pricing_plan.value}"
            )
        except Exception as e:
            ConsoleUI.display_error(f"Ошибка продления подписки: {e}")

    def show_studio_info(self):
        """Показать информацию о студии."""
        if not self.current_studio:
            ConsoleUI.display_error("Не выбрана студия.")
            return

        # Загружаем связанную подписку, чтобы проверить её статус
        subscription = None
        if self.current_studio.has_subscription():
            subscription = self.subscription_repo.find_by_id(
                self.current_studio.subscription_id
            )

        ConsoleUI.display_studio_info(self.current_studio, subscription)

    def update_personal_info(self):
        """Обновление персональной информации пользователя."""
        if not self.current_user:
            ConsoleUI.display_error("Пользователь не авторизован.")
            # Возврат к главной странице
            return  # или self.show_landing_page() если нужно сбросить сессию

        # Определяем роль пользователя *сейчас*, чтобы вернуться в правильное меню
        studios = self.studio_service.get_studios_for_user(self.current_user.id)
        is_owner = False
        is_potential_buyer = False

        if not studios:
            is_potential_buyer = True
        else:
            for studio in studios:
                membership = self.membership_repo.find_by_user_and_studio(
                    self.current_user.id, studio.id
                )
                if membership and UserRoleEnum.OWNER in membership.roles:
                    is_owner = True
                    break

        try:
            current_pi = self.current_user.personal_info
            new_data = ConsoleUI.get_personal_info_update_data(current_pi)
            # Импортируем PersonalInfo, если еще не импортирован в начале файла
            # from src.value_objects.value_objects import PersonalInfo
            personal_info = PersonalInfo(**new_data)
            self.user_service.update_user_personal_info(
                self.current_user.id, personal_info
            )
            ConsoleUI.display_success("Персональная информация успешно обновлена.")
            # Возвращаемся в меню, соответствующее роли пользователя *до* обновления
            # Так как обновление персональных данных не меняет членство в студиях,
            # логика определения роли остается той же.
            if is_owner:
                self.show_owner_dashboard()
            elif is_potential_buyer:
                self.show_potential_buyer_menu()
            else:  # клиент или сотрудник
                # Можно вернуть в меню выбора студии или в главное меню владельца,
                # в зависимости от ожидаемого поведения. Пока вернем в check_user_role.
                # Но так как он не владелец и не ПП, логично вернуть в выбор студии.
                self.show_client_or_employee_menu()
                # Или self.check_user_role(), но это может быть избыточно.
                # self.check_user_role()
        except Exception as e:
            ConsoleUI.display_error(f"Ошибка обновления персональной информации: {e}")
            # После ошибки тоже логично вернуться в меню, соответствующее роли
            if is_owner:
                self.show_owner_dashboard()
            elif is_potential_buyer:
                self.show_potential_buyer_menu()
            else:  # клиент или сотрудник
                self.show_client_or_employee_menu()

    def logout(self):
        """Выход из аккаунта."""
        if self.current_user:
            ConsoleUI.display_logout_message(self.current_user.contact_info.email.value)
            self.current_user = None
            self.current_studio = None


def main():
    """Главная функция запуска консольного приложения."""
    app = ConsoleApp()
    app.run()


if __name__ == "__main__":
    main()
