import redis
from redis.exceptions import ConnectionError, TimeoutError
import logging
import time

from ..config.settings import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """
    Redis-клиент с повторными попытками подключения
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                logger.info(f"📡 Попытка подключения к Redis ({attempt + 1}/{max_retries})...")
                logger.debug(
                    f"Параметры подключения: host={settings.REDIS_HOST}, port={settings.REDIS_PORT}, db={settings.REDIS_DB}"
                )

                self.client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD,
                    socket_timeout=2,
                    socket_connect_timeout=2,
                    retry_on_timeout=True,
                    decode_responses=True,
                )

                # Проверка соединения
                self.client.ping()
                logger.info(
                    f"✅ Успешное подключение к Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}"
                )
                self._initialized = True
                return

            except (ConnectionError, TimeoutError) as e:
                logger.warning(f"⚠️ Не удалось подключиться к Redis: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"⏳ Повторная попытка через {retry_delay} секунд...")
                    time.sleep(retry_delay)
                else:
                    logger.error("❌ Все попытки подключения к Redis исчерпаны")
                    raise ConnectionError(
                        "Не удалось подключиться к Redis после нескольких попыток"
                    )
            except Exception as e:
                logger.exception(f"❌ Неожиданная ошибка при подключении к Redis: {str(e)}")
                raise

    def get(self, key: str) -> str | None:
        try:
            logger.debug(f"🔍 GET из Redis: {key}")
            result = self.client.get(key)
            logger.debug(f"✅ Получено значение: {result}")
            return result
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"❌ Ошибка при GET операции: {str(e)}")
            return None
        except Exception as e:
            logger.exception(f"❌ Неожиданная ошибка в GET операции: {str(e)}")
            return None

    def setex(self, key: str, seconds: int, value: str) -> bool:
        try:
            logger.debug(f"💾 SETEX в Redis: {key} = {value} (TTL: {seconds} сек)")
            result = self.client.setex(key, seconds, value)
            logger.debug(f"✅ SETEX результат: {result}")
            return result
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"❌ Ошибка при SETEX операции: {str(e)}")
            return False
        except Exception as e:
            logger.exception(f"❌ Неожиданная ошибка в SETEX операции: {str(e)}")
            return False
