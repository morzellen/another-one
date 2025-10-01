from entities import *
from value_objects import *
from datetime import datetime, timedelta
from uuid import uuid4
from decimal import Decimal


def print_entity_state(entity, entity_name):
    """Выводит информацию о сущности в человеко-читаемом формате"""
    print(f"\n{'='*50}")
    print(f"Состояние {entity_name}:")
    print(f"{'='*50}")

    if isinstance(entity, Studio):
        print(f"ID студии: {entity.id}")
        print(f"Имя студии: {entity.name}")
        print(f"ID владельца: {entity.owner_id}")
        print(
            f"Политика скидок: {entity.discount_policy.discount_percent * 100}% для статуса {entity.discount_policy.required_status.value if entity.discount_policy.required_status else 'любой'}"
        )
        print(f"Создана: {entity.created_at}")

    elif isinstance(entity, User):
        print(f"ID пользователя: {entity.id}")
        print(f"ID студии: {entity.studio_id}")
        print(
            f"Контактная информация: Email - {entity.contact_info.email}, Телефон - {entity.contact_info.phone}"
        )
        print(
            f"Персональная информация: {entity.personal_info.first_name} {entity.personal_info.last_name}"
        )
        print(f"Статус пользователя: {entity.status.value}")
        print(f"Роли: {[role.value for role in entity.roles]}")
        print(f"Создан: {entity.created_at}")

    elif isinstance(entity, Project):
        print(f"ID проекта: {entity.id}")
        print(f"ID студии: {entity.studio_id}")
        print(f"ID клиента: {entity.client_id}")
        print(f"Статус проекта: {entity.status.value}")
        print(f"Количество подпроектов: {len(entity.subprojects_ids)}")
        print(f"Количество комментариев: {len(entity.comments_ids)}")
        print(f"Количество файлов: {len(entity.files_ids)}")
        print(f"Создан: {entity.created_at}")

    elif isinstance(entity, SubProject):
        print(f"ID подпроекта: {entity.id}")
        print(f"ID проекта: {entity.project_id}")
        print(f"ID студии: {entity.studio_id}")
        print(f"Тип услуги: {entity.service_type.value}")
        print(f"Статус подпроекта: {entity.status.value}")
        print(f"ID создателя: {entity.created_by}")
        print(f"Количество задач: {len(entity.tasks_ids)}")
        print(f"Количество файлов: {len(entity.files_ids)}")
        print(f"Создан: {entity.updated_at}")

    elif isinstance(entity, Booking):
        print(f"ID бронирования: {entity.id}")
        print(f"ID студии: {entity.studio_id}")
        print(f"ID клиента: {entity.client_id}")
        print(f"Тип услуги: {entity.service_type.value}")
        print(f"Статус бронирования: {entity.status.value}")
        print(f"Статус оплаты: {entity.payment_status.value}")
        print(f"Метод оплаты: {entity.payment_method.value}")
        print(f"Время начала: {entity.start_time}")
        print(f"Время окончания: {entity.end_time}")
        print(f"ID назначенного сотрудника: {entity.assigned_employee_id}")
        print(f"Создано: {entity.created_at}")

    elif isinstance(entity, Task):
        print(f"ID задачи: {entity.id}")
        print(f"ID подпроекта: {entity.subproject_id}")
        print(f"Заголовок: {entity.title}")
        print(f"Описание: {entity.description}")
        print(f"Статус задачи: {entity.status.value}")
        print(f"ID создателя: {entity.created_by}")
        print(f"Создана: {entity.created_at}")

    elif isinstance(entity, File):
        print(f"ID файла: {entity.id}")
        print(f"ID проекта: {entity.project_id}")
        print(f"ID подпроекта: {entity.subproject_id}")
        print(f"Тип файла: {entity.file_type.value}")
        print(f"Формат файла: {entity.format.value}")
        print(f"URL файла: {entity.url}")
        print(f"ID загрузившего: {entity.uploaded_by}")
        print(f"Загружен: {entity.uploaded_at}")

    elif isinstance(entity, Comment):
        print(f"ID комментария: {entity.id}")
        print(f"ID проекта: {entity.project_id}")
        print(f"Текст комментария: {entity.text}")
        print(f"ID оставившего: {entity.left_by}")
        print(f"Создан: {entity.created_at}")


def create_studio_system():
    """Создает систему с двумя студиями и всеми необходимыми сущностями"""
    print("Создание системы управления студией звукозаписи...")

    # Создаем две студии
    studio1_id = uuid4()
    studio2_id = uuid4()

    # Владельцы студий
    owner1_id = uuid4()
    owner2_id = uuid4()

    # Создаем политики скидок
    discount_policy1 = DiscountPolicy(
        studio_id=studio1_id,
        discount_percent=Decimal("0.15"),  # 15% скидка
        required_status=UserStatusesEnum.VIP,
        min_tracks=5,
        period_days=365,
        created_at=datetime.now(),
    )

    discount_policy2 = DiscountPolicy(
        studio_id=studio2_id,
        discount_percent=Decimal("0.10"),  # 10% скидка
        required_status=UserStatusesEnum.ACTIVE,
        min_tracks=3,
        period_days=180,
        created_at=datetime.now(),
    )

    # Создаем студии
    studio1 = Studio(
        id=studio1_id,
        owner_id=owner1_id,
        name="Музыкальная Студия Harmony",
        discount_policy=discount_policy1,
        created_at=datetime.now(),
    )

    studio2 = Studio(
        id=studio2_id,
        owner_id=owner2_id,
        name="Звуковая Лаборатория SoundLab",
        discount_policy=discount_policy2,
        created_at=datetime.now(),
    )

    print_entity_state(studio1, "первой студии")
    print_entity_state(studio2, "второй студии")

    return studio1, studio2, owner1_id, owner2_id


def create_users(studio1, studio2, owner1_id, owner2_id):
    """Создает пользователей для обеих студий"""
    print("\nСоздание пользователей...")

    # Владельцы
    owner1 = User(
        id=owner1_id,
        studio_id=studio1.id,
        contact_info=ContactInfo(email="owner1@harmony.com", phone="+1234567890"),
        personal_info=PersonalInfo(
            first_name="Алексей", last_name="Владельцев", bio="Владелец студии Harmony"
        ),
        status=UserStatusesEnum.ACTIVE,
        roles={UserRoleEnum.OWNER},
        created_at=datetime.now(),
    )

    owner2 = User(
        id=owner2_id,
        studio_id=studio2.id,
        contact_info=ContactInfo(email="owner2@soundlab.com", phone="+0987654321"),
        personal_info=PersonalInfo(
            first_name="Мария", last_name="Владелина", bio="Владелец студии SoundLab"
        ),
        status=UserStatusesEnum.ACTIVE,
        roles={UserRoleEnum.OWNER},
        created_at=datetime.now(),
    )

    # Клиенты
    client1_id = uuid4()
    client2_id = uuid4()
    client3_id = uuid4()

    client1 = User(
        id=client1_id,
        studio_id=studio1.id,
        contact_info=ContactInfo(email="client1@music.com", phone="+1111111111"),
        personal_info=PersonalInfo(
            first_name="Иван", last_name="Музыкант", bio="Индивидуальный исполнитель"
        ),
        status=UserStatusesEnum.NEW,
        roles={UserRoleEnum.CLIENT},
        created_at=datetime.now(),
    )

    client2 = User(
        id=client2_id,
        studio_id=studio1.id,
        contact_info=ContactInfo(email="client2@band.com", phone="+2222222222"),
        personal_info=PersonalInfo(
            first_name="Группа", last_name="Рокеры", bio="Рок-группа"
        ),
        status=UserStatusesEnum.ACTIVE,
        roles={UserRoleEnum.CLIENT},
        created_at=datetime.now(),
    )

    client3 = User(
        id=client3_id,
        studio_id=studio2.id,
        contact_info=ContactInfo(email="client3@hiphop.com", phone="+3333333333"),
        personal_info=PersonalInfo(
            first_name="Рэпер", last_name="Микрофон", bio="Хип-хоп артист"
        ),
        status=UserStatusesEnum.VIP,
        roles={UserRoleEnum.CLIENT},
        created_at=datetime.now(),
    )

    # Инженеры
    engineer1_id = uuid4()
    engineer2_id = uuid4()

    engineer1 = User(
        id=engineer1_id,
        studio_id=studio1.id,
        contact_info=ContactInfo(email="engineer1@harmony.com", phone="+4444444444"),
        personal_info=PersonalInfo(
            first_name="Максим",
            last_name="Микшер",
            bio="Профессиональный звукорежиссер",
        ),
        status=UserStatusesEnum.ACTIVE,
        roles={UserRoleEnum.ENGINEER},
        created_at=datetime.now(),
    )

    engineer2 = User(
        id=engineer2_id,
        studio_id=studio2.id,
        contact_info=ContactInfo(email="engineer2@soundlab.com", phone="+5555555555"),
        personal_info=PersonalInfo(
            first_name="Анна", last_name="Мастер", bio="Мастеринг-инженер"
        ),
        status=UserStatusesEnum.ACTIVE,
        roles={UserRoleEnum.ENGINEER},
        created_at=datetime.now(),
    )

    # Дизайнеры
    designer1_id = uuid4()
    designer2_id = uuid4()

    designer1 = User(
        id=designer1_id,
        studio_id=studio1.id,
        contact_info=ContactInfo(email="designer1@harmony.com", phone="+6666666666"),
        personal_info=PersonalInfo(
            first_name="Елена", last_name="Художница", bio="Дизайнер обложек"
        ),
        status=UserStatusesEnum.ACTIVE,
        roles={UserRoleEnum.DESIGNER},
        created_at=datetime.now(),
    )

    designer2 = User(
        id=designer2_id,
        studio_id=studio2.id,
        contact_info=ContactInfo(email="designer2@soundlab.com", phone="+7777777777"),
        personal_info=PersonalInfo(
            first_name="Дмитрий", last_name="Творец", bio="Видео-дизайнер"
        ),
        status=UserStatusesEnum.ACTIVE,
        roles={UserRoleEnum.DESIGNER},
        created_at=datetime.now(),
    )

    users = [
        owner1,
        owner2,
        client1,
        client2,
        client3,
        engineer1,
        engineer2,
        designer1,
        designer2,
    ]

    for user in users:
        print_entity_state(
            user,
            f"пользователя {user.personal_info.first_name} {user.personal_info.last_name}",
        )

    return {
        "owner1": owner1,
        "owner2": owner2,
        "client1": client1,
        "client2": client2,
        "client3": client3,
        "engineer1": engineer1,
        "engineer2": engineer2,
        "designer1": designer1,
        "designer2": designer2,
    }


def create_profiles(users):
    """Создает профили для пользователей"""
    print("\nСоздание профилей пользователей...")

    # Профили клиентов
    client_profile1 = ClientProfile(user_id=users["client1"].id)
    client_profile2 = ClientProfile(user_id=users["client2"].id)
    client_profile3 = ClientProfile(user_id=users["client3"].id)

    # Профили инженеров
    engineer_profile1 = EngineerProfile(
        user_id=users["engineer1"].id,
        employee_info=EmployeeInfo(
            specialties=[ServicesTypesEnum.MIXING, ServicesTypesEnum.MASTERING],
            hourly_rate=Decimal("50.00"),
            portfolio_url="https://engineer1.com/portfolio",
        ),
    )

    engineer_profile2 = EngineerProfile(
        user_id=users["engineer2"].id,
        employee_info=EmployeeInfo(
            specialties=[ServicesTypesEnum.MASTERING, ServicesTypesEnum.RECORDING],
            hourly_rate=Decimal("60.00"),
            portfolio_url="https://engineer2.com/portfolio",
        ),
    )

    # Профили дизайнеров
    designer_profile1 = DesignerProfile(
        user_id=users["designer1"].id,
        employee_info=EmployeeInfo(
            specialties=[ServicesTypesEnum.DESIGNING],
            hourly_rate=Decimal("35.00"),
            portfolio_url="https://designer1.com/portfolio",
        ),
        design_style_ids=[uuid4(), uuid4()],  # ID стилей дизайна
    )

    designer_profile2 = DesignerProfile(
        user_id=users["designer2"].id,
        employee_info=EmployeeInfo(
            specialties=[ServicesTypesEnum.DESIGNING],
            hourly_rate=Decimal("40.00"),
            portfolio_url="https://designer2.com/portfolio",
        ),
        design_style_ids=[uuid4()],
    )

    # Профили владельцев
    owner_profile1 = OwnerProfile(user_id=users["owner1"].id)
    owner_profile2 = OwnerProfile(user_id=users["owner2"].id)

    profiles = {
        "client1": client_profile1,
        "client2": client_profile2,
        "client3": client_profile3,
        "engineer1": engineer_profile1,
        "engineer2": engineer_profile2,
        "designer1": designer_profile1,
        "designer2": designer_profile2,
        "owner1": owner_profile1,
        "owner2": owner_profile2,
    }

    print("Профили успешно созданы для всех пользователей")
    return profiles


def create_projects_and_bookings(users, studio1, studio2):
    """Создает проекты и бронирования"""
    print("\nСоздание проектов и бронирований...")

    # Создаем проекты для студии 1
    project1_id = uuid4()
    project1 = Project(
        id=project1_id,
        studio_id=studio1.id,
        client_id=users["client1"].id,
        created_by=users["client1"].id,
        created_at=datetime.now(),
        status=ProjectStatusesEnum.ACTIVE,
    )

    project2_id = uuid4()
    project2 = Project(
        id=project2_id,
        studio_id=studio1.id,
        client_id=users["client2"].id,
        created_by=users["owner1"].id,
        created_at=datetime.now(),
        status=ProjectStatusesEnum.DRAFT,
    )

    # Создаем проекты для студии 2
    project3_id = uuid4()
    project3 = Project(
        id=project3_id,
        studio_id=studio2.id,
        client_id=users["client3"].id,
        created_by=users["client3"].id,
        created_at=datetime.now(),
        status=ProjectStatusesEnum.ACTIVE,
    )

    print_entity_state(project1, "проекта клиента 1")
    print_entity_state(project2, "проекта клиента 2")
    print_entity_state(project3, "проекта клиента 3")

    # Создаем бронирования
    booking1_id = uuid4()
    booking1 = Booking(
        id=booking1_id,
        studio_id=studio1.id,
        client_id=users["client1"].id,
        service_type=ServicesTypesForBookingEnum.RECORDING,
        start_time=datetime.now() + timedelta(hours=2),
        end_time=datetime.now() + timedelta(hours=4),
        assigned_employee_id=users["engineer1"].id,
        created_at=datetime.now(),
        status=BookingStatusesEnum.CONFIRMED,
        payment_status=PaymentStatusesEnum.PAID,
        payment_method=PaymentMethodsEnum.CARD,
    )

    booking2_id = uuid4()
    booking2 = Booking(
        id=booking2_id,
        studio_id=studio1.id,
        client_id=users["client2"].id,
        service_type=ServicesTypesForBookingEnum.MIXING,
        start_time=datetime.now() + timedelta(days=1),
        end_time=datetime.now() + timedelta(days=1, hours=3),
        assigned_employee_id=users["engineer1"].id,
        created_at=datetime.now(),
        status=BookingStatusesEnum.CREATED,
        payment_status=PaymentStatusesEnum.UNPAID,
        payment_method=PaymentMethodsEnum.CASH,
    )

    booking3_id = uuid4()
    booking3 = Booking(
        id=booking3_id,
        studio_id=studio2.id,
        client_id=users["client3"].id,
        service_type=ServicesTypesForBookingEnum.MASTERING,
        start_time=datetime.now() + timedelta(days=2),
        end_time=datetime.now() + timedelta(days=2, hours=2),
        assigned_employee_id=users["engineer2"].id,
        created_at=datetime.now(),
        status=BookingStatusesEnum.CONFIRMED,
        payment_status=PaymentStatusesEnum.PAID,
        payment_method=PaymentMethodsEnum.CARD,
        project_id=project3_id,
    )

    print_entity_state(booking1, "бронирования 1")
    print_entity_state(booking2, "бронирования 2")
    print_entity_state(booking3, "бронирования 3")

    return [project1, project2, project3], [booking1, booking2, booking3]


def create_subprojects_and_tasks(projects, users, studio1, studio2):
    """Создает подпроекты и задачи"""
    print("\nСоздание подпроектов и задач...")

    # Создаем подпроекты
    subproject1_id = uuid4()
    subproject1 = SubProject(
        id=subproject1_id,
        studio_id=studio1.id,
        project_id=projects[0].id,  # проект клиента 1
        created_by=users["engineer1"].id,
        updated_at=datetime.now(),
        service_type=ServicesTypesEnum.RECORDING,
        booking_id=None,
        status=SubProjectStatusesEnum.IN_PROGRESS,
    )

    subproject2_id = uuid4()
    subproject2 = SubProject(
        id=subproject2_id,
        studio_id=studio1.id,
        project_id=projects[0].id,  # проект клиента 1
        created_by=users["designer1"].id,
        updated_at=datetime.now(),
        service_type=ServicesTypesEnum.DESIGNING,
        booking_id=None,
        status=SubProjectStatusesEnum.ASSIGNED,
    )

    subproject3_id = uuid4()
    subproject3 = SubProject(
        id=subproject3_id,
        studio_id=studio2.id,
        project_id=projects[2].id,  # проект клиента 3
        created_by=users["engineer2"].id,
        updated_at=datetime.now(),
        service_type=ServicesTypesEnum.MASTERING,
        booking_id=None,
        status=SubProjectStatusesEnum.COMPLETED,
    )

    print_entity_state(subproject1, "подпроекта 1")
    print_entity_state(subproject2, "подпроекта 2")
    print_entity_state(subproject3, "подпроекта 3")

    # Создаем задачи
    task1_id = uuid4()
    task1 = Task(
        id=task1_id,
        subproject_id=subproject1.id,
        title="Записать основной вокал",
        created_by=users["engineer1"].id,
        created_at=datetime.now(),
        description="Записать вокальные партии для песни 'Новая мечта'",
        status=TaskStatusesEnum.IN_PROGRESS,
    )

    task2_id = uuid4()
    task2 = Task(
        id=task2_id,
        subproject_id=subproject1.id,
        title="Записать гитарные партии",
        created_by=users["engineer1"].id,
        created_at=datetime.now(),
        description="Записать ритм- и соло-гитару",
        status=TaskStatusesEnum.NEW,
    )

    task3_id = uuid4()
    task3 = Task(
        id=task3_id,
        subproject_id=subproject2.id,
        title="Создать обложку альбома",
        created_by=users["designer1"].id,
        created_at=datetime.now(),
        description="Создать минималистичную обложку в стиле 'новая волна'",
        status=TaskStatusesEnum.NEW,
    )

    task4_id = uuid4()
    task4 = Task(
        id=task4_id,
        subproject_id=subproject3.id,
        title="Финальный мастеринг",
        created_by=users["engineer2"].id,
        created_at=datetime.now(),
        description="Применить мастеринг к альбому 'Городские истории'",
        status=TaskStatusesEnum.COMPLETED,
    )

    print_entity_state(task1, "задачи 1")
    print_entity_state(task2, "задачи 2")
    print_entity_state(task3, "задачи 3")
    print_entity_state(task4, "задачи 4")

    # Обновляем подпроекты с ID задач
    subproject1.tasks_ids = [task1.id, task2.id]
    subproject2.tasks_ids = [task3.id]
    subproject3.tasks_ids = [task4.id]

    return [subproject1, subproject2, subproject3], [task1, task2, task3, task4]


def create_files_and_comments(projects, subprojects, users):
    """Создает файлы и комментарии"""
    print("\nСоздание файлов и комментариев...")

    # Создаем файлы
    file1_id = uuid4()
    file1 = File(
        id=file1_id,
        project_id=projects[0].id,
        subproject_id=subprojects[0].id,
        uploaded_by=users["client1"].id,
        uploaded_at=datetime.now(),
        file_type=FileTypesEnum.AUDIO,
        format=FileFormatEnum.WAV,
        url="https://storage.com/projects/1/tracks/main_vocal.wav",
    )

    file2_id = uuid4()
    file2 = File(
        id=file2_id,
        project_id=projects[0].id,
        subproject_id=subprojects[0].id,
        uploaded_by=users["engineer1"].id,
        uploaded_at=datetime.now(),
        file_type=FileTypesEnum.AUDIO,
        format=FileFormatEnum.MP3,
        url="https://storage.com/projects/1/tracks/recorded_vocal.mp3",
    )

    file3_id = uuid4()
    file3 = File(
        id=file3_id,
        project_id=projects[0].id,
        subproject_id=subprojects[1].id,
        uploaded_by=users["designer1"].id,
        uploaded_at=datetime.now(),
        file_type=FileTypesEnum.IMAGE,
        format=FileFormatEnum.PNG,
        url="https://storage.com/projects/1/design/cover_draft.png",
    )

    file4_id = uuid4()
    file4 = File(
        id=file4_id,
        project_id=projects[2].id,
        subproject_id=subprojects[2].id,
        uploaded_by=users["engineer2"].id,
        uploaded_at=datetime.now(),
        file_type=FileTypesEnum.AUDIO,
        format=FileFormatEnum.WAV,
        url="https://storage.com/projects/3/mastered_album.wav",
    )

    print_entity_state(file1, "файла 1")
    print_entity_state(file2, "файла 2")
    print_entity_state(file3, "файла 3")
    print_entity_state(file4, "файла 4")

    # Создаем комментарии
    comment1_id = uuid4()
    comment1 = Comment(
        id=comment1_id,
        studio_id=projects[0].studio_id,
        project_id=projects[0].id,
        left_by=users["client1"].id,
        text="Пожалуйста, добавьте реверберацию к вокалу, как в примере на Spotify",
        created_at=datetime.now(),
    )

    comment2_id = uuid4()
    comment2 = Comment(
        id=comment2_id,
        studio_id=projects[0].studio_id,
        project_id=projects[0].id,
        left_by=users["owner1"].id,
        text="Инженер, обратите внимание на комментарий клиента по обработке вокала",
        created_at=datetime.now(),
    )

    comment3_id = uuid4()
    comment3 = Comment(
        id=comment3_id,
        studio_id=projects[2].studio_id,
        project_id=projects[2].id,
        left_by=users["client3"].id,
        text="Отличная работа! Альбом звучит потрясающе, спасибо за профессионализм!",
        created_at=datetime.now(),
    )

    print_entity_state(comment1, "комментария 1")
    print_entity_state(comment2, "комментария 2")
    print_entity_state(comment3, "комментария 3")

    # Обновляем проекты с ID файлов и комментариев
    projects[0].files_ids = [file1.id, file2.id, file3.id]
    projects[0].comments_ids = [comment1.id, comment2.id]
    projects[2].files_ids = [file4.id]
    projects[2].comments_ids = [comment3.id]

    return [file1, file2, file3, file4], [comment1, comment2, comment3]


def simulate_scenarios(
    studio1, studio2, users, projects, bookings, subprojects, tasks, files, comments
):
    """Симулирует различные сценарии работы системы"""
    print("\n" + "=" * 60)
    print("СИМУЛЯЦИЯ РАБОТЫ СИСТЕМЫ - ВАРИАНТЫ РАЗВИТИЯ СОБЫТИЙ")
    print("=" * 60)

    print("\n--- СЦЕНАРИЙ 1: Клиент создает бронирование и проект ---")
    print(
        f"Клиент {users['client2'].personal_info.first_name} {users['client2'].personal_info.last_name} создает новое бронирование для записи"
    )

    new_booking_id = uuid4()
    new_booking = Booking(
        id=new_booking_id,
        studio_id=studio1.id,
        client_id=users["client2"].id,
        service_type=ServicesTypesForBookingEnum.RECORDING,
        start_time=datetime.now() + timedelta(days=3),
        end_time=datetime.now() + timedelta(days=3, hours=4),
        assigned_employee_id=users["engineer1"].id,
        created_at=datetime.now(),
        status=BookingStatusesEnum.CREATED,
        payment_status=PaymentStatusesEnum.UNPAID,
        payment_method=PaymentMethodsEnum.CARD,
    )

    print_entity_state(new_booking, "нового бронирования клиента 2")

    print(f"Бронирование автоматически создает новый проект для клиента")
    new_project_id = uuid4()
    new_project = Project(
        id=new_project_id,
        studio_id=studio1.id,
        client_id=users["client2"].id,
        created_by=users["client2"].id,
        created_at=datetime.now(),
        status=ProjectStatusesEnum.ACTIVE,
        subprojects_ids=[],
        comments_ids=[],
        files_ids=[],
    )

    print_entity_state(new_project, "нового проекта клиента 2")

    print("\n--- СЦЕНАРИЙ 2: Владелец подтверждает бронирование ---")
    print(
        f"Владелец {users['owner1'].personal_info.first_name} подтверждает бронирование клиента"
    )
    new_booking.status = BookingStatusesEnum.CONFIRMED
    new_booking.confirmed_at = datetime.now()
    print(f"Статус бронирования изменен на: {new_booking.status.value}")
    print(f"Бронирование подтверждено: {new_booking.confirmed_at}")

    print("\n--- СЦЕНАРИЙ 3: Инженер создает подпроект для работы ---")
    print(
        f"Инженер {users['engineer1'].personal_info.first_name} создает подпроект для записи"
    )

    new_subproject_id = uuid4()
    new_subproject = SubProject(
        id=new_subproject_id,
        studio_id=studio1.id,
        project_id=new_project.id,
        created_by=users["engineer1"].id,
        updated_at=datetime.now(),
        service_type=ServicesTypesEnum.RECORDING,
        booking_id=new_booking.id,
        status=SubProjectStatusesEnum.ASSIGNED,
    )

    new_project.subprojects_ids.append(new_subproject.id)
    new_booking.project_id = new_project.id

    print_entity_state(new_subproject, "нового подпроекта инженера")
    print_entity_state(new_project, "обновленного проекта")
    print_entity_state(new_booking, "обновленного бронирования")

    print("\n--- СЦЕНАРИЙ 4: Инженер добавляет задачи в подпроект ---")
    print(f"Инженер добавляет задачи в подпроект")

    task5_id = uuid4()
    task5 = Task(
        id=task5_id,
        subproject_id=new_subproject.id,
        title="Подготовить оборудование",
        created_by=users["engineer1"].id,
        created_at=datetime.now(),
        description="Настроить микрофоны и оборудование для записи",
        status=TaskStatusesEnum.NEW,
    )

    task6_id = uuid4()
    task6 = Task(
        id=task6_id,
        subproject_id=new_subproject.id,
        title="Записать барабаны",
        created_by=users["engineer1"].id,
        created_at=datetime.now(),
        description="Записать барабанные партии для всех песен",
        status=TaskStatusesEnum.NEW,
    )

    new_subproject.tasks_ids = [task5.id, task6.id]

    print_entity_state(task5, "новой задачи 5")
    print_entity_state(task6, "новой задачи 6")
    print(f"Подпроект теперь содержит {len(new_subproject.tasks_ids)} задач")

    print("\n--- СЦЕНАРИЙ 5: Клиент загружает файл в проект ---")
    print(
        f"Клиент {users['client2'].personal_info.first_name} загружает демозапись в проект"
    )

    file5_id = uuid4()
    file5 = File(
        id=file5_id,
        project_id=new_project.id,
        subproject_id=new_subproject.id,
        uploaded_by=users["client2"].id,
        uploaded_at=datetime.now(),
        file_type=FileTypesEnum.AUDIO,
        format=FileFormatEnum.MP3,
        url="https://storage.com/projects/5/demo_track.mp3",
    )

    new_project.files_ids.append(file5.id)
    new_subproject.files_ids.append(file5.id)

    print_entity_state(file5, "загруженного файла")
    print(f"Проект теперь содержит {len(new_project.files_ids)} файлов")

    print("\n--- СЦЕНАРИЙ 6: Клиент добавляет комментарий к проекту ---")
    print(f"Клиент оставляет комментарий с пожеланиями по записи")

    comment4_id = uuid4()
    comment4 = Comment(
        id=comment4_id,
        studio_id=new_project.studio_id,
        project_id=new_project.id,
        left_by=users["client2"].id,
        text="Пожалуйста, используйте ламповый компрессор для вокала, как в классических записях",
        created_at=datetime.now(),
    )

    new_project.comments_ids.append(comment4.id)

    print_entity_state(comment4, "нового комментария")
    print(f"Проект теперь содержит {len(new_project.comments_ids)} комментариев")

    print("\n--- СЦЕНАРИЙ 7: Инженер начинает работу и меняет статус задач ---")
    print(f"Инженер начинает выполнение задач и меняет их статусы")

    task5.status = TaskStatusesEnum.IN_PROGRESS
    task5.updated_at = datetime.now()
    print(f"Задача '{task5.title}' переведена в статус: {task5.status.value}")

    task6.status = TaskStatusesEnum.COMPLETED
    task6.completed_at = datetime.now()
    task6.updated_at = datetime.now()
    print(f"Задача '{task6.title}' завершена: {task6.completed_at}")

    print("\n--- СЦЕНАРИЙ 8: Подпроект переводится в статус 'в процессе' ---")
    print(f"Подпроект переводится в статус 'в процессе' работы")

    new_subproject.status = SubProjectStatusesEnum.IN_PROGRESS
    new_subproject.updated_at = datetime.now()
    print(f"Статус подпроекта изменен на: {new_subproject.status.value}")

    print("\n--- СЦЕНАРИЙ 9: Клиент отменяет бронирование ---")
    print(
        f"Клиент {users['client2'].personal_info.first_name} отменяет бронирование из-за форс-мажора"
    )

    new_booking.status = BookingStatusesEnum.CANCELLED
    new_booking.cancelled_at = datetime.now()
    print(f"Бронирование отменено: {new_booking.cancelled_at}")
    print(f"Новый статус бронирования: {new_booking.status.value}")

    print("\n--- СЦЕНАРИЙ 10: Владелец применяет скидку VIP-клиенту ---")
    print(
        f"Клиент {users['client3'].personal_info.first_name} является VIP-клиентом и получает скидку"
    )

    vip_discount = studio2.discount_policy.discount_percent * 100
    print(f"VIP-клиент получает скидку: {vip_discount}% на следующие услуги")
    print(
        f"Условия скидки: для статуса {studio2.discount_policy.required_status.value}, минимум {studio2.discount_policy.min_tracks} треков за {studio2.discount_policy.period_days} дней"
    )

    print("\n--- СЦЕНАРИЙ 11: Проект завершается и архивируется ---")
    print(f"Проект клиента 3 завершается и переводится в архив")

    projects[2].status = ProjectStatusesEnum.COMPLETED
    projects[2].completed_at = datetime.now()
    print(f"Проект завершен: {projects[2].completed_at}")
    print(f"Статус проекта: {projects[2].status.value}")

    projects[2].status = ProjectStatusesEnum.ARCHIVED
    projects[2].archived_at = datetime.now()
    print(f"Проект архивирован: {projects[2].archived_at}")
    print(f"Финальный статус проекта: {projects[2].status.value}")

    print("\n--- СЦЕНАРИЙ 12: Дизайнер создает подпроект для оформления ---")
    print(
        f"Дизайнер {users['designer2'].personal_info.first_name} создает подпроект для оформления альбома"
    )

    design_subproject_id = uuid4()
    design_subproject = SubProject(
        id=design_subproject_id,
        studio_id=studio2.id,
        project_id=projects[2].id,
        created_by=users["designer2"].id,
        updated_at=datetime.now(),
        service_type=ServicesTypesEnum.DESIGNING,
        booking_id=None,
        status=SubProjectStatusesEnum.ASSIGNED,
    )

    print_entity_state(design_subproject, "подпроекта дизайна")

    print("\n--- СЦЕНАРИЙ 13: Клиент оплачивает услуги ---")
    print(
        f"Клиент {users['client1'].personal_info.first_name} оплачивает завершенные услуги"
    )

    bookings[0].payment_status = PaymentStatusesEnum.PAID
    print(
        f"Оплата за бронирование {bookings[0].id} статус: {bookings[0].payment_status.value}"
    )

    print("\n--- СЦЕНАРИЙ 14: Статус клиента повышается до VIP ---")
    print(f"Клиент {users['client2'].personal_info.first_name} достигает статуса VIP")

    users["client2"].status = UserStatusesEnum.VIP
    print(f"Новый статус клиента: {users['client2'].status.value}")

    print("\n--- СЦЕНАРИЙ 15: Владелец создает системные уведомления ---")
    print(f"Владелец отправляет уведомления участникам проекта")

    notification_comment = Comment(
        id=uuid4(),
        studio_id=studio1.id,
        project_id=new_project.id,
        left_by=users["owner1"].id,
        text="Важное уведомление: Студия будет закрыта на профилактику в следующий понедельник",
        created_at=datetime.now(),
    )

    new_project.comments_ids.append(notification_comment.id)
    print(f"Добавлено системное уведомление: {notification_comment.text}")


def main():
    print("ЗАПУСК СИМУЛЯЦИИ СИСТЕМЫ УПРАВЛЕНИЯ СТУДИЕЙ ЗВУКОЗАПИСИ")
    print("=" * 60)

    # Создаем систему
    studio1, studio2, owner1_id, owner2_id = create_studio_system()

    # Создаем пользователей
    users = create_users(studio1, studio2, owner1_id, owner2_id)

    # Создаем профили
    profiles = create_profiles(users)

    # Создаем проекты и бронирования
    projects, bookings = create_projects_and_bookings(users, studio1, studio2)

    # Создаем подпроекты и задачи
    subprojects, tasks = create_subprojects_and_tasks(projects, users, studio1, studio2)

    # Создаем файлы и комментарии
    files, comments = create_files_and_comments(projects, subprojects, users)

    # Симулируем различные сценарии
    simulate_scenarios(
        studio1, studio2, users, projects, bookings, subprojects, tasks, files, comments
    )

    print("\n" + "=" * 60)
    print("СИМУЛЯЦИЯ ЗАВЕРШЕНА")
    print("Все возможные сценарии работы системы продемонстрированы")
    print("=" * 60)


if __name__ == "__main__":
    main()
