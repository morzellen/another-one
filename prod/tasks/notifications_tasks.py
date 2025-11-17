from celery import shared_task
from ..infrastructure.notifications.telegram_notifier import TelegramNotifier
from ..infrastructure.redis_client import RedisClient
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue="notifications")  # 1 минута
def send_telegram_notification(self, event_type: str, event_data: dict):
    """
    Асинхронная отправка уведомлений в Telegram

    Обрабатывает:
    - Ошибки сети
    - Перегрузку Telegram API
    - Отсутствие chat_id пользователя
    """
    try:
        # TODO: использовать DI
        redis_client = RedisClient()
        notifier = TelegramNotifier(redis_client=redis_client)

        # TODO: обработка события через EventBus
        # события будут десериализованы из event_data и переданы в EventBus.publish()

    except Exception as exc:
        logger.error(f"Task failed: {str(exc)}")
        raise self.retry(exc=exc)


@shared_task(queue="analytics")
def log_event_analytics(event_type: str, event_data: dict):
    """
    Асинхронная запись аналитики событий
    """
    # TODO: реализация отправки в систему аналитики
    pass
