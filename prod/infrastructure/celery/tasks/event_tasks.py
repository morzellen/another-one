from celery import shared_task
import logging
from datetime import datetime
from uuid import UUID

from ..application.services.event_bus import EventBus

logger = logging.getLogger(__name__)


@shared_task(queue="events")
def handle_domain_event(event_data):
    """
    Обработка доменных событий, полученных через Celery

    Этот метод запускается в том же процессе, где работает TelegramNotifier,
    поэтому EventBus имеет доступ ко всем зарегистрированным обработчикам
    """
    logger.info(f"📥 Получено событие через Celery: {event_data['event_type']}")
    logger.debug(f"🧩 Данные события: {event_data}")

    try:
        # Восстановление объекта события из словаря
        event_class = globals()[event_data["event_type"]]

        # Создание объекта события
        event_kwargs = event_data["data"].copy()
        event_kwargs["event_id"] = UUID(event_kwargs["event_id"])
        event_kwargs["occurred_at"] = datetime.fromisoformat(event_kwargs["occurred_at"])

        event = event_class(**event_kwargs)

        # Публикация события локальному EventBus
        logger.info(f"🔔 Публикация события локальному EventBus: {event.__class__.__name__}")
        EventBus.publish(event)
        logger.info(f"✅ Событие успешно обработано: {event.__class__.__name__}")

    except KeyError as e:
        logger.error(f"❌ Неизвестный тип события: {event_data['event_type']}")
    except Exception as e:
        logger.exception(f"❌ Ошибка при обработке события: {str(e)}")
        raise
