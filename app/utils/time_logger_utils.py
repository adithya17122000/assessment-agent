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

                if elapsed < 1:
                    duration = f"{elapsed * 1000:.2f} ms"
                elif elapsed < 60:
                    duration = f"{elapsed:.2f} sec"
                else:
                    mins, secs = divmod(elapsed, 60)
                    duration = f"{int(mins)} min {secs:.2f} sec"

                logger.info("[PERF] %s took %s", name or func.__qualname__, duration)

        return wrapper
    return decorator