import logging
import pytest

from src.libs.retry_tool import retry
from src.libs.project_logger import logger


class ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


def _attach_list_handler(level=logging.INFO):
    handler = ListHandler()
    prev_level = logger.level
    logger.setLevel(level)
    logger.addHandler(handler)
    return handler, prev_level


def _detach_list_handler(handler: logging.Handler, prev_level):
    try:
        logger.removeHandler(handler)
    finally:
        logger.setLevel(prev_level)


def test_retry_success_sync():
    handler, prev_level = _attach_list_handler()
    try:
        attempts = {"n": 0}

        @retry(retry_time=3)
        def flaky():
            attempts["n"] += 1
            if attempts["n"] < 3:
                raise ValueError("temporary error")
            return "ok"

        assert flaky() == "ok"
        assert attempts["n"] == 3

        messages = [r.getMessage() for r in handler.records]
        warn_msgs = [m for m in messages if "[RETRY]" in m and "attempt=" in m and "error=" in m]
        assert len(warn_msgs) == 2
        assert "attempt=1/3" in warn_msgs[0]
        assert "attempt=2/3" in warn_msgs[1]
        assert not any("exhausted attempts" in m for m in messages)
    finally:
        _detach_list_handler(handler, prev_level)


def test_retry_exhaust_sync():
    handler, prev_level = _attach_list_handler()
    try:
        @retry(retry_time=2)
        def always_fail():
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError):
            always_fail()

        messages = [r.getMessage() for r in handler.records]
        warn_msgs = [m for m in messages if "[RETRY]" in m and "attempt=" in m and "error=" in m]
        err_msgs = [m for m in messages if "[RETRY]" in m and "exhausted attempts" in m]
        assert any("attempt=1/2" in m for m in warn_msgs)
        assert any("exhausted attempts=2" in m for m in err_msgs)
    finally:
        _detach_list_handler(handler, prev_level)


@pytest.mark.asyncio
async def test_retry_success_async():
    handler, prev_level = _attach_list_handler()
    try:
        attempts = {"n": 0}

        @retry(retry_time=3)
        async def flaky_async():
            attempts["n"] += 1
            if attempts["n"] < 3:
                raise ValueError("temporary error")
            return "ok"

        assert await flaky_async() == "ok"
        assert attempts["n"] == 3

        messages = [r.getMessage() for r in handler.records]
        warn_msgs = [m for m in messages if "[RETRY]" in m and "attempt=" in m and "error=" in m]
        assert len(warn_msgs) == 2
        assert any("attempt=1/3" in m for m in warn_msgs)
        assert any("attempt=2/3" in m for m in warn_msgs)
    finally:
        _detach_list_handler(handler, prev_level)
