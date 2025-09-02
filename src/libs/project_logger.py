import logging
from pathlib import Path
from datetime import datetime

# Compute project root (three levels up from this file: src/libs/log)
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_LOG_DIR = _PROJECT_ROOT / "log"
_LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log filename with current timestamp: yyyymmddhhmmss.log
_LOG_FILE = _LOG_DIR / f"{datetime.now().strftime('%Y%m%d%H%M%S')}.log"

# Create a module-level logger
logger = logging.getLogger("project_logger")
logger.setLevel(logging.INFO)
logger.propagate = False  # avoid duplicate messages if root logger has handlers

# Attach handlers only once
if not logger.handlers:
    file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Include filename, function name, and line number
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(funcName)s:%(lineno)d) - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Also log to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

__all__ = []
