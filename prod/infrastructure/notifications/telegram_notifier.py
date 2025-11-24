import logging
import requests
from typing import Dict, Any

from ...domain.bookings.booking_events import BookingConfirmedEvent, BookingCancelledEvent
from ...application.services.event_bus import EventBus
from .retry_mechanism import with_retry

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """
    Сервис уведомлений через Telegram с поддержкой кэширования и retry-логикой
    """

    _instance = None

    def __new__(cls, bot_token: str, redis_client):
        if cls._instance is None:
            cls._instance = super(TelegramNotifier, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, bot_token: str, redis_client):
        if self._initialized:
            return

        logger.info("🔧 Инициализация TelegramNotifier...")

        self.bot_token = bot_token
        self.redis_client = redis_client
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        # Проверка валидности токена (БАЗОВЫЙ МИНИМУМ, ПХХПХП TODO: ДОБАВИТЬ ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ)
        if not bot_token or len(bot_token) < 10:
            logger.warning("⚠️ Telegram бот токен выглядит некорректно")

        self._register_event_handlers()
        self._initialized = True
        logger.info("✅ TelegramNotifier успешно инициализирован")

    def _register_event_handlers(self) -> None:
        """Регистрация обработчиков для доменных событий"""
        logger.debug("📝 Регистрация обработчиков событий...")

        EventBus.subscribe(BookingConfirmedEvent, self._handle_booking_confirmed)
        EventBus.subscribe(BookingCancelledEvent, self._handle_booking_cancelled)

        logger.debug("✅ Обработчики событий зарегистрированы")

    def _get_cached_chat_id(self, user_id: str) -> int | None:
        """Получение chat_id из Redis-кэша"""
        logger.debug(f"🔍 Поиск chat_id для пользователя: {user_id}")
        cached = self.redis_client.get(f"telegram:chat_id:{user_id}")

        if cached:
            logger.debug(f"✅ Найден кэшированный chat_id: {cached}")
            return int(cached)

        logger.warning(f"❌ Chat ID не найден в кэше для пользователя: {user_id}")
        return None

    @with_retry(max_attempts=3, base_delay=1.0, max_delay=10.0)
    def _send_telegram_message(self, chat_id: int, text: str) -> Dict[str, Any]:
        """Отправка сообщения в Telegram с retry-механизмом"""
        logger.info(f"📤 Отправка сообщения в Telegram чат {chat_id}")
        logger.debug(f"📝 Текст сообщения: {text}")

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        try:
            logger.debug(f"📡 Отправка запроса в Telegram API: {payload}")
            response = requests.post(
                self.base_url, json=payload, timeout=(3.05, 15)  # connect timeout, read timeout
            )
            response.raise_for_status()
            result = response.json()

            if result.get("ok"):
                logger.info("✅ Сообщение успешно отправлено в Telegram")
                logger.debug(f"📥 Ответ от Telegram API: {result}")
                return result
            else:
                error_msg = result.get("description", "Неизвестная ошибка Telegram API")
                logger.error(f"❌ Ошибка Telegram API: {error_msg}")
                raise Exception(f"Telegram API error: {error_msg}")

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Ошибка сети при отправке в Telegram: {str(e)}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"📜 Тело ответа: {e.response.text}")
            raise
        except Exception as e:
            logger.exception(f"❌ Неожиданная ошибка при отправке сообщения: {str(e)}")
            raise

    def _handle_booking_confirmed(self, event: BookingConfirmedEvent) -> None:
        """Обработка события подтверждения бронирования"""
        logger.info(f"🔔 Получено событие подтверждения бронирования: {event.booking_id}")
        logger.debug(f"📊 Данные события: {event}")

        chat_id = self._get_cached_chat_id(str(event.client_id))

        if not chat_id:
            logger.error(
                f"❌ Не удалось отправить уведомление: chat_id не найден для клиента {event.client_id}"
            )
            logger.info(
                '💡 Совет: Добавьте chat_id в Redis: redis-cli SET "telegram:chat_id:{client_id}" ваш_chat_id'
            )
            return

        message = (
            f"✅ <b>Бронирование подтверждено!</b>\n\n"
            f"🆔 Бронь: {event.booking_id}\n"
            f"🎵 Студия: {event.studio_id}\n"
            f"📅 Дата: {event.time_range_start.strftime('%d.%m.%Y')}\n"
            f"⏰ Время: {event.time_range_start.strftime('%H:%M')} - "
            f"{event.time_range_end.strftime('%H:%M')}\n\n"
            f"Для управления бронированием используйте команду /bookings"
        )

        try:
            self._send_telegram_message(chat_id, message)
            logger.info(f"✅ Уведомление о подтверждении отправлено клиенту {event.client_id}")
        except Exception as e:
            logger.error(f"❌ Не удалось отправить уведомление: {str(e)}")

    def _handle_booking_cancelled(self, event: BookingCancelledEvent) -> None:
        """Обработка события отмены бронирования"""
        logger.info(f"🔔 Получено событие отмены бронирования: {event.booking_id}")

        chat_id = self._get_cached_chat_id(str(event.client_id))

        if not chat_id:
            logger.error(
                f"❌ Не удалось отправить уведомление об отмене: chat_id не найден для клиента {event.client_id}"
            )
            return

        message = (
            f"❌ <b>Бронирование отменено</b>\n\n"
            f"🆔 Бронь: {event.booking_id}\n"
            f"❗ Причина: {event.reason}\n\n"
            f"Для повторного бронирования используйте /book_new"
        )

        try:
            self._send_telegram_message(chat_id, message)
            logger.info(f"✅ Уведомление об отмене отправлено клиенту {event.client_id}")
        except Exception as e:
            logger.error(f"❌ Не удалось отправить уведомление об отмене: {str(e)}")
