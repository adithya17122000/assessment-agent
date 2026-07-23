import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

def timeit(name=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                logger.info(
                    "[PERF] %s took %.2f ms",
                    name or func.__qualname__,
                    elapsed * 1000,
                )

        return wrapper
    return decorator