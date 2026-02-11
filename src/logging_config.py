import logging
import os
import sys
import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

import colorlog

from src.constants import LOG_FILE_PATH

logger = logging.getLogger("python-template")
logger.setLevel(logging.INFO)

try:
    os.remove(LOG_FILE_PATH)
except OSError:
    pass


if not logger.handlers:
    handler = colorlog.StreamHandler(sys.stdout)
    handler_file = logging.FileHandler(LOG_FILE_PATH)

    formatter = colorlog.ColoredFormatter(
        fmt=(
            "%(asctime)s "
            "[%(log_color)s%(levelname)s%(reset)s] "
            "%(filename)s: %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )

    formatter_file = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(filename)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)
    handler_file.setFormatter(formatter_file)

    logger.addHandler(handler)
    logger.addHandler(handler_file)
    logger.propagate = True


def set_level(level: int) -> None:
    logger.setLevel(level)


P = ParamSpec("P")
T = TypeVar("T")


def log_performance(fn: Callable[P, T]) -> Callable[P, T]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        logger.info(f"[{fn.__qualname__}] started.")
        start = time.monotonic()
        result = fn(*args, **kwargs)
        elapsed = time.monotonic() - start
        logger.info(f"[{fn.__qualname__}] finished in {elapsed:.4f}s")
        return result

    return wrapper
