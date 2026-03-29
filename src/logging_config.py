import datetime
import inspect
import logging
import logging.config
import os
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, ParamSpec, TypeVar

import yaml

from src.config import get_settings

settings = get_settings()


def _get_log_dir(log_dir: str) -> Path:
    """
    Resolve the configured log directory under the base log directory and
    ensure it cannot escape `_BASE_LOG_DIR` via absolute paths or `..` segments.
    """
    candidate = (_BASE_LOG_DIR / log_dir).resolve()
    try:
        # raises ValueError if `candidate` is not within `_BASE_LOG_DIR`
        candidate.relative_to(_BASE_LOG_DIR)
    except ValueError as exc:
        raise ValueError(
            f"Invalid log_dir '{log_dir}': must resolve inside '{_BASE_LOG_DIR}'."
        ) from exc
    return candidate


_LOGGER_NAME = "root"
_CONFIG_PATH = Path(__file__).resolve().parent.parent / "configs" / "logger.yaml"
_BASE_LOG_DIR = Path(__file__).resolve().parent.parent / "logs"

_LOG_DIR = _get_log_dir(settings.log_dir)
_LOG_FILENAME = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".log"
_LOG_PATH = _LOG_DIR / _LOG_FILENAME

os.makedirs(_LOG_DIR, exist_ok=True)


def _load_dict_config() -> dict[str, Any]:
    raw = _CONFIG_PATH.read_text(encoding="utf-8")
    config: dict[str, Any] = yaml.safe_load(raw)
    config["handlers"]["file"]["filename"] = _LOG_PATH
    return config


logging.config.dictConfig(_load_dict_config())
logger = logging.getLogger(_LOGGER_NAME)


def set_level(level: int) -> None:
    logger.setLevel(level)


P = ParamSpec("P")
T = TypeVar("T")


def log_performance(
    *, log_args: list[str] | None = None
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(fn: Callable[P, T]) -> Callable[P, T]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            selected = {}
            if log_args:
                signature = inspect.signature(fn)
                bound = signature.bind(*args, **kwargs)
                bound.apply_defaults()
                selected = {
                    name: bound.arguments[name]
                    for name in log_args
                    if name in bound.arguments
                }
            arg_string = (
                "["
                + ", ".join([f"{key}={repr(value)}" for key, value in selected.items()])
                + "]"
            )

            fully_qualified_name = fn.__module__ + "." + fn.__qualname__
            logger.info(f"[{fully_qualified_name}] started with args: {arg_string}")

            start = time.monotonic()
            result = fn(*args, **kwargs)
            elapsed = time.monotonic() - start

            logger.info(f"[{fully_qualified_name}] finished in {elapsed:.4f}s")
            return result

        return wrapper

    return decorator
