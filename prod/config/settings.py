from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Настройки приложения с загрузкой из .env файла
    """

    # Telegram
    TELEGRAM_BOT_TOKEN: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: Optional[str]

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Logging
    LOG_LEVEL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
