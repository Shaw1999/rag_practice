from __future__ import annotations

import asyncio
import inspect
from datetime import datetime
from functools import wraps
from pathlib import Path
from time import perf_counter

from src.libs.project_logger import logger


def _format_dt(dt: datetime) -> str:
    # e.g. 2025-09-03 10:30:45.123456
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")


def record_time(func):
    """Decorator to record and log execution time for a function.

    Log format (single line):
      [TIME] file=<filename> func=<qualname> start=<YYYY-mm-dd HH:MM:SS.ffffff> end=<...> duration_s=<seconds>

    Works for both sync and async functions.
    """

    file_name = Path(inspect.getfile(func)).name
    func_name = func.__qualname__

    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def _async_wrapped(*args, **kwargs):
            start_dt = datetime.now()
            start = perf_counter()
            ok = False
            try:
                result = await func(*args, **kwargs)
                ok = True
                return result
            finally:
                end_dt = datetime.now()
                duration = perf_counter() - start
                logger.info(
                    "[TIME] file=%s func=%s start=%s end=%s duration_s=%.6f status=%s",
                    file_name,
                    func_name,
                    _format_dt(start_dt),
                    _format_dt(end_dt),
                    duration,
                    "ok" if ok else "error",
                )

        return _async_wrapped

    @wraps(func)
    def _wrapped(*args, **kwargs):
        start_dt = datetime.now()
        start = perf_counter()
        ok = False
        try:
            result = func(*args, **kwargs)
            ok = True
            return result
        finally:
            end_dt = datetime.now()
            duration = perf_counter() - start
            logger.info(
                "[TIME] file=%s func=%s start=%s end=%s duration_s=%.6f status=%s",
                file_name,
                func_name,
                _format_dt(start_dt),
                _format_dt(end_dt),
                duration,
                "ok" if ok else "error",
            )

    return _wrapped


__all__ = ["record_time"]
