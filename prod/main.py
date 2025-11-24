import logging
from .config.settings import settings

from uuid import uuid4, UUID
from datetime import datetime, timezone
from .domain.bookings.booking import Booking
from .domain.bookings.value_objects.booking_time_range_vo import BookingTimeRange
from .domain.bookings.booking_enums import BookingServicesTypesEnum
from .infrastructure.redis_client import RedisClient
from .infrastructure.notifications.telegram_notifier import TelegramNotifier

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def init_notification_system():
    """Инициализация системы уведомлений при старте приложения"""
    try:
        logger.info("🚀 Инициализация системы уведомлений...")
        logger.debug(f"TELEGRAM_BOT_TOKEN начинается с: {settings.TELEGRAM_BOT_TOKEN[:5]}...")

        # Инициализация Redis
        redis_client = RedisClient()
        logger.info("✅ Redis клиент инициализирован")

        # Инициализация Telegram Notifier
        notifier = TelegramNotifier(settings.TELEGRAM_BOT_TOKEN, redis_client)
        logger.info("✅ Telegram Notifier инициализирован")

        logger.info("✅ Система уведомлений успешно инициализирована")
        logger.info("🔧 Система запущена и ожидает событий...")
        logger.info("💡 Используйте 'test' для запуска теста подтверждения бронирования")
        logger.info("💡 Используйте 'quit' для выхода")

        return redis_client, notifier

    except Exception as e:
        logger.exception(f"❌ КРИТИЧЕСКАЯ ОШИБКА при инициализации: {str(e)}")
        raise


def run_test():
    """Запуск теста подтверждения бронирования в текущем процессе"""
    logger.info("🧪 Запуск теста подтверждения бронирования...")

    TEST_CLIENT_ID = UUID("11111111-2222-3333-4444-555555555555")

    # Создание временного диапазона
    time_range = BookingTimeRange(
        start_time=datetime(2025, 11, 25, 15, 0, tzinfo=timezone.utc),
        end_time=datetime(2025, 11, 25, 17, 0, tzinfo=timezone.utc),
    )

    logger.info("🆕 Создание нового бронирования...")
    booking = Booking(
        id=uuid4(),
        studio_id=uuid4(),
        client_id=TEST_CLIENT_ID,
        assigned_employee_id=uuid4(),
        service_type=BookingServicesTypesEnum.MIXING,
        time_range=time_range,
        created_at=datetime.now(timezone.utc),
    )
    logger.info(f"✅ Бронирование создано: {booking.id}")
    logger.info(f"👤 Клиент ID: {TEST_CLIENT_ID}")
    logger.info("🔧 Подтверждение бронирования...")

    # Подтверждение бронирования (событие будет отправлено в Celery)
    booking_service.confirm(booking, confirmed_at=datetime.now(timezone.utc))

    logger.info("✅ Тест завершен успешно!")


if __name__ == "__main__":
    redis_client, notifier = init_notification_system()
    try:
        while True:
            user_input = input("\nВведите команду (test/quit): ").strip().lower()
            if user_input == "quit":
                logger.info("🛑 Получен сигнал остановки...")
                break
            elif user_input == "test":
                run_test()
            else:
                logger.info("💡 Доступные команды: 'test' - тест подтверждения, 'quit' - выход")
    except KeyboardInterrupt:
        logger.info("🛑 Получен сигнал остановки (Ctrl+C)...")
    logger.info("✅ Система уведомлений остановлена")
