"""
Модуль для работы с пользовательским интерфейсом консольного приложения.
Содержит методы для отображения меню, получения ввода пользователя и вывода информации.
"""

import textwrap
from typing import List, Optional, Tuple
from ..entities.user import User
from ..entities.studio import Studio
from ..entities.subscription import Subscription
from ..domain.enums import PricingPlanEnum
from ..constants import PRICES_FOR_SUB_PLANS


class ConsoleUI:
    """Класс для взаимодействия с пользователем через консоль."""

    @staticmethod
    def display_welcome():
        """Отображает приветственное сообщение."""
        welcome_msg = textwrap.dedent(
            """
            === Добро пожаловать в ASMSR Product Landing Page ===
            """
        ).strip()
        print(f"\n{welcome_msg}\n")

    @staticmethod
    def get_main_action() -> str:
        """Запрашивает у пользователя действие на главной странице."""
        # TODO: Передать динамические данные о продукте
        print(
            textwrap.dedent(
                """
                *Информация о продукте*
                
                1. Вход
                2. Регистрация
                3. Назад
                """
            ).strip()
        )
        return input("Введите номер действия: ").strip()

    # TODO:
    # Изменить логику на такую:
    # Подгрузить динамически список провайдеров
    #
    # 1)
    # Выберите, через что войти:
    # 0. Вход по логину/паролю (отобразить вместо native)
    # 1. google
    # 2. yandex
    # 3. vk
    # 4. telegram
    #
    # 2)
    # Если выбран 0, то get_native_login_credentials()
    # Если выбран другой провайдер, то get_oauth2_login_credentials()

    @staticmethod
    def get_login_method() -> str:
        """Запрашивает способ входа."""
        print(
            textwrap.dedent(
                """
                Выберите способ входа:
                1. Вход по нативному логину/паролю
                2. Вход OAuth2
                3. Назад
                """
            ).strip()
        )
        return input("Введите номер способа: ").strip()

    @staticmethod
    def get_native_login_credentials() -> Tuple[str, str]:
        """Запрашивает логин и пароль для нативного входа."""
        return (
            input(
                "Введите логин (email, никнейм или номер телефона): "
            ).strip(),  # TODO: Добавить возможность ввода номера телефона/никнейма на бэкенде
            input("Введите пароль: ").strip(),
        )

    @staticmethod
    def get_oauth2_login_credentials() -> str:
        """Запрашивает провайдера и токен для OAuth2 входа."""
        return input("Введите токен: ").strip()

    @staticmethod
    def get_registration_credentials() -> Tuple[str, str]:
        """Запрашивает данные для регистрации."""
        return (
            input(
                "Введите логин (email или номер телефона): "
            ).strip(),  # TODO: Добавить возможность ввода номера телефона на бэкенде
            input("Введите пароль: ").strip(),
        )

    @staticmethod
    def get_user_action_for_role(is_owner: bool, is_potential_buyer: bool) -> str:
        """
        Запрашивает действие пользователя и отображает
        возможные действия в зависимости от его роли.
        """
        if is_owner:
            print(
                textwrap.dedent(
                    """
                    1. Студия
                    2. Личный кабинет
                    3. Выйти из аккаунта
                    """
                ).strip()
            )
        elif is_potential_buyer:
            print(
                textwrap.dedent(
                    """
                    1. Личный кабинет
                    2. Выйти из аккаунта
                    """
                ).strip()
            )
        else:  # клиент или сотрудник
            print(
                textwrap.dedent(
                    """
                    1. Студия
                    2. Выйти из аккаунта
                    """
                ).strip()
            )
        return input("Введите номер действия: ").strip()

    @staticmethod
    def get_potential_buyer_action() -> str:
        """Запрашивает действие для потенциального покупателя."""
        print(
            textwrap.dedent(
                """
                1. Назад
                2. Создать студию
                3. Настроить информацию о себе
                """
            ).strip()
        )
        return input("Введите номер действия: ").strip()

    @staticmethod
    def get_studio_creation_data() -> str:
        """Запрашивает данные для создания студии."""
        return input("\nВведите название студии: ").strip()

    @staticmethod
    def display_studio_created_success(studio: Studio, subscription: Optional[Subscription] = None):
        """Отображает сообщение об успешном создании студии."""
        if subscription:
            if subscription.is_trial():
                status = "TRIAL"
                expires_at = subscription.period.end_time
            elif subscription.is_lifetime():
                status = "LIFETIME"
                expires_at = None
            else:
                status = subscription.pricing_plan.value
                expires_at = subscription.period.end_time
        else:
            status = "Без подписки"
            expires_at = None

        message = textwrap.dedent(
            f"""
            🎉 Поздравляем! Ваша студия '{studio.name}' готова к работе.
            Статус: {status}
            """
        ).strip()
        print(f"\n{message}")

        if expires_at:
            print(f"Подписка истекает: {expires_at}")

        print("\nТеперь вы — Владелец студии.")

    @staticmethod
    def get_owner_action() -> str:
        """Запрашивает действие для владельца."""
        print(
            textwrap.dedent(
                """
                *Информация о продукте*
                Вы вошли как Владелец студии.
                Что вы хотите сделать дальше?
                1. Студия
                2. Личный кабинет Владельца
                3. Выйти из аккаунта
                """
            ).strip()
        )
        return input("Введите номер действия: ").strip()

    @staticmethod
    def get_owner_dashboard_action() -> str:
        """Запрашивает действие в личном кабинете владельца."""
        print(
            textwrap.dedent(
                """
                *Контактная, персональная информация, а также инфо о подписках и функционале*
                Выберите действие:
                1. Назад
                2. Продлить подписку
                3. Настроить информацию о себе
                """
            ).strip()
        )
        return input("Введите номер действия: ").strip()

    @staticmethod
    def get_client_or_employee_action() -> str:
        """Запрашивает действие для клиента или сотрудника."""
        print(
            textwrap.dedent(
                """
                *Информация о продукте*
                Вы вошли как клиент или сотрудник.
                Что вы хотите сделать дальше?
                1. Студия
                2. Выйти из аккаунта
                """
            ).strip()
        )
        return input("Введите номер действия: ").strip()

    @staticmethod
    def select_studio(studios: List[Studio]) -> Optional[Studio]:
        """Позволяет пользователю выбрать студию из списка."""
        if not studios:
            print("У вас нет доступа ни к одной студии.")
            return None
        print("\nВыберите доступную студию:")
        for i, studio in enumerate(studios, 1):
            print(f"{i}. {studio.name}")
        print(f"{len(studios) + 1}. Назад")
        choice = input("Введите номер студии: ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(studios):
                return studios[index]
            else:
                return None
        except ValueError:
            print("Неверный формат. Попробуйте снова.")
            return None

    @staticmethod
    def display_studio_menu(
        studio: Studio,
        roles: List[str],
        functionality: List[str],
        subscription: Optional[Subscription] = None,
    ):
        """Отображает меню выбранной студии."""
        roles_str = ", ".join(roles)
        functionality_str = ", ".join(functionality)

        menu_lines = [
            f"Вы находитесь в студии: {studio.name}",
            f"Ваши роли в этой студии: {roles_str}",
            f"Доступный функционал: {functionality_str}",
        ]

        if subscription:
            if subscription.is_trial():
                menu_lines.append(f"Статус подписки: TRIAL (до {subscription.period.end_time})")
            elif subscription.is_lifetime():
                menu_lines.append("Статус подписки: LIFETIME")
            else:
                menu_lines.append(
                    f"Статус подписки: {subscription.pricing_plan.value} (до {subscription.period.end_time})"
                )

        menu_lines.extend(
            [
                "",
                "Выберите действие:",
                "1. Назад",
                "2. Настроить студию",
                "3. Управление подпиской",
                "4. Просмотреть информацию о студии",
            ]
        )

        menu_text = "\n".join(menu_lines)
        print(f"\n{menu_text}")

    @staticmethod
    def get_studio_management_action() -> str:
        """Запрашивает действие для управления студией."""
        return input("Введите номер действия: ").strip()

    @staticmethod
    def get_configure_studio_action() -> str:
        """Запрашивает действие для настройки студии."""
        print(
            textwrap.dedent(
                """
                Настройка студии:
                Что вы хотите изменить?
                1. Название студии
                2. Описание студии
                3. Логотип студии
                4. Политика скидок
                5. Назад
                """
            ).strip()
        )
        return input("Введите номер действия: ").strip()

    @staticmethod
    def get_new_studio_name() -> str:
        """Запрашивает новое название студии."""
        new_name = input("Введите новое название: ").strip()
        if not new_name:
            raise ValueError("Название не может быть пустым.")
        return new_name

    @staticmethod
    def get_new_studio_description() -> str:
        """Запрашивает новое описание студии."""
        return input("Введите описание студии: ").strip()

    @staticmethod
    def get_new_studio_logo_url() -> str:
        """Запрашивает новый URL логотипа студии."""
        return input("Введите URL логотипа: ").strip()

    @staticmethod
    def get_subscription_management_action() -> str:
        """Запрашивает действие для управления подпиской."""
        print(
            textwrap.dedent(
                """
                Управление подпиской:
                Выберите действие:
                1. Назад
                2. Продлить подписку
                3. Просмотреть цены
                """
            ).strip()
        )
        return input("Введите номер действия: ").strip()

    @staticmethod
    def get_trial_days() -> int:
        """Запрашивает количество дней для пробного периода."""
        days_input = input("Введите количество дней пробного периода (по умолчанию 14): ").strip()
        return int(days_input) if days_input else 14

    @staticmethod
    def get_pricing_plan() -> PricingPlanEnum:
        """Запрашивает выбор тарифного плана."""
        print(
            textwrap.dedent(
                """
                Выберите тип подписки:
                1. BASIC (9.99$)
                2. PRO (29.99$)
                3. LIFETIME (99.99$)
                4. Назад
                """
            ).strip()
        )
        choice = input("Введите номер подписки: ").strip()
        if choice == "1":
            return PricingPlanEnum.BASIC
        elif choice == "2":
            return PricingPlanEnum.PRO
        elif choice == "3":
            return PricingPlanEnum.LIFETIME
        else:
            raise ValueError("Неверный выбор.")

    @staticmethod
    def display_pricing():
        """Отображает цены на подписки."""
        print("\nЦены на подписки:")
        for plan, price in PRICES_FOR_SUB_PLANS.items():
            print(f"{plan.value}: {price}$")

    @staticmethod
    def display_studio_info(studio: Studio, subscription: Optional[Subscription] = None):
        """Отображает подробную информацию о студии."""
        info_lines = [
            f"Информация о студии: {studio.name}",
            f"Владелец: {studio.owner_id}",
            f"Дата создания: {studio.created_at}",
        ]

        if studio.updated_at:
            info_lines.append(f"Дата последнего обновления: {studio.updated_at}")

        if subscription:
            if subscription.is_trial():
                info_lines.append(f"Подписка: TRIAL (до {subscription.period.end_time})")
            elif subscription.is_lifetime():
                info_lines.append("Подписка: LIFETIME")
            else:
                info_lines.append(
                    f"Подписка: {subscription.pricing_plan.value} (до {subscription.period.end_time})"
                )
        else:
            info_lines.append("Подписка: Не активирована")

        info_text = "\n".join(info_lines)
        print(f"\n{info_text}")

    @staticmethod
    def get_personal_info_update_data(current_pi) -> dict:
        """Запрашивает данные для обновления персональной информации."""
        current_first = current_pi.first_name if current_pi else ""
        current_last = current_pi.last_name if current_pi else ""
        current_patronymic = current_pi.patronymic if current_pi else ""
        current_avatar = current_pi.avatar_url if current_pi else ""
        current_bio = current_pi.bio if current_pi else ""

        personal_info_menu = textwrap.dedent(
            f"""
            Текущие данные:
            Имя ({current_first}): 
            Фамилия ({current_last}): 
            Отчество ({current_patronymic}): 
            URL аватара ({current_avatar}): 
            Биография ({current_bio}): 
            """
        ).strip()
        print(personal_info_menu)

        first_name = input(f"Имя ({current_first}): ").strip() or current_first
        last_name = input(f"Фамилия ({current_last}): ").strip() or current_last
        patronymic = input(f"Отчество ({current_patronymic}): ").strip() or current_patronymic
        avatar_url = input(f"URL аватара ({current_avatar}): ").strip() or current_avatar
        bio = input(f"Биография ({current_bio}): ").strip() or current_bio

        return {
            "first_name": first_name or None,
            "last_name": last_name or None,
            "patronymic": patronymic or None,
            "avatar_url": avatar_url or None,
            "bio": bio or None,
        }

    @staticmethod
    def display_logout_message(email: str):
        """Отображает сообщение о выходе из аккаунта."""
        print(f"\nВы вышли из аккаунта {email}.")

    @staticmethod
    def display_error(message: str):
        """Отображает сообщение об ошибке."""
        print(f"❌ Ошибка: {message}")

    @staticmethod
    def display_success(message: str):
        """Отображает сообщение об успехе."""
        print(f"✅ Успех: {message}")

    @staticmethod
    def display_info(message: str):
        """Отображает информационное сообщение."""
        print(f"ℹ️ Информация: {message}")

    @staticmethod
    def display_warning(message: str):
        """Отображает предупреждение."""
        print(f"⚠️ Предупреждение: {message}")

    @staticmethod
    def wait_for_enter():
        """Ждет нажатия Enter."""
        input("\nНажмите Enter, чтобы продолжить...")
