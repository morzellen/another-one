from typing import Callable, Dict, List
import logging

logger = logging.getLogger(__name__)


class EventBus:
    """
    Локальная шина событий для обработки событий внутри одного процесса
    """

    _subscribers: Dict[type, List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_type: type, handler: Callable) -> None:
        """Регистрация обработчика для конкретного типа события"""
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(handler)
        logger.debug(f"✅ Зарегистрирован обработчик для события {event_type.__name__}")

    @classmethod
    def publish(cls, event) -> None:
        """Публикация события всем заинтересованным подписчикам в текущем процессе"""
        logger.info(f"🔔 Локальная публикация события: {event.__class__.__name__}")

        event_type = type(event)
        handlers = cls._subscribers.get(event_type, [])

        if not handlers:
            logger.warning(f"⚠️ Нет обработчиков для события: {event_type.__name__}")
            return

        logger.debug(f"📬 Найдено обработчиков для {event_type.__name__}: {len(handlers)}")

        for handler in handlers:
            try:
                logger.debug(f"⚙️ Выполнение обработчика: {handler.__name__}")
                handler(event)
                logger.debug(f"✅ Обработчик выполнен успешно: {handler.__name__}")
            except Exception as e:
                logger.exception(f"❌ Ошибка в обработчике {handler.__name__}: {str(e)}")
                # Не прерываем обработку других подписчиков при ошибке одного
