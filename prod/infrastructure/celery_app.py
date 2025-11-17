import platform
from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger
import logging

from ..config.settings import settings


def init_celery() -> Celery:
    """
    Инициализация Celery с продакшен-настройками
    """
    celery_app = Celery(
        "notifications",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=[
            "prod.tasks.notifications_tasks",
            "prod.tasks.event_tasks",
        ],
    )

    def get_celery_pool():
        """Определение пула воркеров в зависимости от ОС"""
        if platform.system().lower() == "windows":
            # используем solo пул для избежания проблем с multiprocessing
            return "solo"
        return "prefork"

    # Продакшен-конфигурация
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_time_limit=300,  # 5 минут
        task_soft_time_limit=240,  # 4 минуты
        worker_prefetch_multiplier=1,  # Оптимизация для I/O-bound задач
        broker_connection_retry_on_startup=True,
        worker_pool=get_celery_pool(),
        task_routes={
            "prod.tasks.notifications_tasks.send_telegram_notification": {"queue": "notifications"},
            "prod.tasks.event_tasks.handle_domain_event": {"queue": "events"},
        },
    )

    return celery_app


# Инициализация
celery_app = init_celery()


@after_setup_logger.connect
@after_setup_task_logger.connect
def setup_loggers(logger, *args, **kwargs):
    """Настройка логирования для Celery"""
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
