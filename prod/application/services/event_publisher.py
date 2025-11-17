import logging
from celery import current_app
from ...tasks.event_tasks import handle_domain_event

logger = logging.getLogger(__name__)


class DistributedEventPublisher:
    """
    Распределенный публикатор событий для межпроцессного взаимодействия
    Использует Celery для доставки событий между процессами
    """

    @staticmethod
    def publish(event):
        """
        Публикация события во все процессы через Celery

        :param event: Объект доменного события
        """
        logger.info(f"🌐 Публикация события во все процессы: {event.__class__.__name__}")
        logger.debug(f"📦 Данные события: {event.__dict__}")

        # Преобразование события в словарь для сериализации
        event_data = {
            "event_type": event.__class__.__name__,
            "event_id": str(event.event_id),
            "occurred_at": event.occurred_at.isoformat(),
            "data": event.__dict__,
        }

        # Отправка задачи в Celery для асинхронной обработки во всех воркерах
        try:
            # Проверяем, доступен ли Celery (если нет, логируем ошибку)
            if current_app.control.inspect().stats():
                handle_domain_event.delay(event_data)
                logger.info(f"✅ Событие отправлено в очередь Celery: {event.__class__.__name__}")
            else:
                logger.warning("⚠️ Celery недоступен, событие будет обработано локально")
                # Локальная обработка при отсутствии Celery
                from .event_bus import EventBus

                EventBus.publish(event)
        except Exception as e:
            logger.exception(f"❌ Ошибка при отправке события в Celery: {str(e)}")
            # Резервная обработка события
            from .event_bus import EventBus

            EventBus.publish(event)
