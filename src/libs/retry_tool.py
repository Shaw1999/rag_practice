from __future__ import annotations

import asyncio
import inspect
from functools import wraps
from pathlib import Path
from typing import Callable, TypeVar, Any

from src.libs.project_logger import logger

T = TypeVar("T")


def retry(retry_time: int = 3) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """A decorator to retry a function when an exception occurs.

    Parameters
    ----------
    retry_time : int
        Number of attempts (including the first call). Must be >= 1.

    Notes
    -----
    - Works for both sync and async functions.
    - Logs each failed attempt and the final failure using the shared logger.
    - Message format example:
      [RETRY] file=foo.py func=MyClass.method attempt=2/3 error=ValueError('msg')
    """
    if retry_time < 1:
        raise ValueError("retry_time must be >= 1")

    def _decorator(func: Callable[..., T]) -> Callable[..., T]:
        file_name = Path(inspect.getfile(func)).name
        func_name = func.__qualname__

        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def _async_wrapper(*args: Any, **kwargs: Any) -> T:
                for attempt in range(1, retry_time + 1):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:  # noqa: BLE001 - intentionally catch to retry
                        logger.warning(
                            "[RETRY] file=%s func=%s attempt=%d/%d error=%r",
                            file_name,
                            func_name,
                            attempt,
                            retry_time,
                            e,
                        )
                        if attempt >= retry_time:
                            logger.error(
                                "[RETRY] file=%s func=%s exhausted attempts=%d; raising",
                                file_name,
                                func_name,
                                retry_time,
                            )
                            raise
                        # small yield to event loop before next attempt
                        await asyncio.sleep(0)

            return _async_wrapper

        @wraps(func)
        def _wrapper(*args: Any, **kwargs: Any) -> T:
            for attempt in range(1, retry_time + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # noqa: BLE001 - intentionally catch to retry
                    logger.warning(
                        "[RETRY] file=%s func=%s attempt=%d/%d error=%r",
                        file_name,
                        func_name,
                        attempt,
                        retry_time,
                        e,
                    )
                    if attempt >= retry_time:
                        logger.error(
                            "[RETRY] file=%s func=%s exhausted attempts=%d; raising",
                            file_name,
                            func_name,
                            retry_time,
                        )
                        raise
            # Unreachable, but satisfies type checkers
            raise RuntimeError("Retry wrapper exited unexpectedly")

        return _wrapper

    return _decorator


__all__ = ["retry"]
