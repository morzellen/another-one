from decimal import Decimal
from .domain.enums import PricingPlanEnum, ServicesTypesEnum, UserRoleEnum

# Словарь ROLE_FUNCTIONALITY задаёт набор разрешённых действий (в виде строк-идентификаторов)
# для каждой роли пользователя в системе. Эти идентификаторы используются в механизмах
# авторизации (например, в permission checks, middleware или сервисах) для контроля доступа.
#
# Принципы именования:
# - Используются глаголы в инфинитиве или глагол + объект (например, "create_project", "upload_file").
# - Действия должны быть атомарными и семантически понятными.
# - Ограничения по типу файлов, принадлежности сущностей («свои» vs «чужие» файлы) и бизнес-логика
#   реализуются на уровне валидации и доменных правил, а не в этом списке разрешений.
#
# Примечания по ролям:
# - CLIENT: может управлять только своими проектами, бронированиями и файлами.
# - DESIGNER / ENGINEER: работают в рамках назначенных им проектов и подпроектов;
#   могут управлять только своими задачами и загруженными ими файлами.
# - OWNER: обладает полными правами; для удобства и явности перечислены все ключевые действия,
#   хотя технически наличие флага вроде "full_system_access" может заменить остальные
#   (но явное перечисление улучшает читаемость и аудит безопасности).

ROLE_FUNCTIONALITY = {
    UserRoleEnum.CLIENT: [
        "create_booking",  # Создание бронирования (автоматически создаёт проект)
        "create_project",  # Создание собственного проекта без бронирования
        "download_file",  # Скачивание файлов из своих проектов/подпроектов
        "upload_file",  # Загрузка файлов в свой проект
        "delete_own_file",  # Удаление только своих файлов
        "cancel_booking",  # Отмена своего бронирования
        "reschedule_booking",  # Перенос времени бронирования
        "edit_personal_info",  # Редактирование базовой информации профиля
        "add_project_comment",  # Добавление комментариев/пожеланий к проекту
        "add_service_to_project",  # Добавление услуг (например, дизайн обложки), что создаёт подпроект
        "upload_to_subproject",  # Загрузка референсов в подпроект (например, изображения для обложки)
        "view_own_projects",  # Просмотр только своих проектов и подпроектов
    ],
    UserRoleEnum.DESIGNER: [
        "create_subproject",  # Создание подпроекта в рамках назначенного проекта
        "download_file",  # Скачивание файлов из подпроекта
        "upload_file",  # Загрузка файлов (jpg, png, mp4, avi) — форматы проверяются отдельно
        "delete_own_file",  # Удаление только своих загруженных файлов
        "mark_subproject_complete",  # Завершение подпроекта при выполнении всех задач
        "edit_personal_info",  # Настройка личных данных и цены за услуги
        "add_task_to_subproject",  # Добавление задач в свой подпроект
        "update_task_status",  # Изменение статуса задач (например, "в работе" → "готово")
        "notify_client",  # Отправка уведомлений клиенту по проекту
        "view_assigned_projects",  # Просмотр только тех проектов, где он задействован
    ],
    UserRoleEnum.ENGINEER: [
        "create_subproject",  # Создание подпроекта (например, для мастеринга)
        "download_file",  # Скачивание аудиофайлов из подпроекта
        "upload_file",  # Загрузка аудиофайлов (mp3, wav) — форматы проверяются отдельно
        "delete_own_file",  # Удаление только своих файлов
        "mark_subproject_complete",  # Завершение подпроекта
        "edit_personal_info",  # Настройка профиля и прайса
        "add_task_to_subproject",  # Добавление технических задач
        "update_task_status",  # Обновление статуса задач
        "notify_client",  # Уведомление клиента о прогрессе
        "view_assigned_projects",  # Просмотр только назначенных проектов
    ],
    UserRoleEnum.OWNER: [
        "manage_users",  # Создание, редактирование, удаление клиентов и сотрудников
        "manage_projects",  # Полное управление проектами: создание, архивация, восстановление
        "manage_bookings",  # Полный контроль над бронированиями: создание, подтверждение, отмена, перенос
        "configure_pricing",  # Настройка цен на услуги и правил скидок (в т.ч. по статусу клиента)
        "view_all_analytics",  # Доступ ко всей статистике, отчётам и аналитике платформы
        "send_notifications",  # Отправка сообщений любому пользователю (клиенту, сотруднику)
        "edit_any_user_profile",  # Редактирование профилей любых пользователей
        "assign_staff_to_projects",  # Назначение дизайнеров/инженеров на проекты и подпроекты
        "full_system_access",  # Явный флаг полного доступа (может использоваться как fallback в проверках)
        "view_all_projects",  # Просмотр всех проектов в системе независимо от принадлежности
    ],
}

"""These services can be selected by clients when creating bookings."""
BOOKING_ALLOWED_SERVICES = {
    ServicesTypesEnum.MIXING,
    ServicesTypesEnum.MASTERING,
    ServicesTypesEnum.BEATMAKING,
    ServicesTypesEnum.PROMOTION,
    ServicesTypesEnum.RECORDING,
    ServicesTypesEnum.DESIGNING,
}


# service: TrialLimitService

# method: can_activate_trial_for_owner
MAX_TRIALS_PER_OWNER = 1


# service: StudioService

# methods: create_studio, activate_trial
TRIAL_PERIOD_IN_DAYS = 7

# method: renew_subscription
SUB_PERIOD_IN_DAYS = 30

# method: get_pricing_for_plan
PRICES_FOR_SUB_PLANS = {
    PricingPlanEnum.TRIAL: Decimal("0.00"),
    PricingPlanEnum.BASIC: Decimal("9.99"),
    PricingPlanEnum.PRO: Decimal("29.99"),
}
