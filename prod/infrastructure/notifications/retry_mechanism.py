import time
import random
import functools
import logging
from typing import Callable, Any, Type

logger = logging.getLogger(__name__)


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    """
    Декоратор для реализации экспоненциальной задержки при повторных попытках

    Параметры:
    - max_attempts: максимальное количество попыток
    - base_delay: начальная задержка в секундах
    - max_delay: максимальная задержка в секундах
    - exceptions: типы исключений для перехвата
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        break

                    # Экспоненциальная задержка с jitter
                    delay = min(base_delay * (2**attempt) + random.uniform(0, 1), max_delay)
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed. "
                        f"Retrying in {delay:.2f}s. Error: {str(e)}"
                    )
                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator
