# from starlette.middleware.exceptions import ExceptionMiddleware as ExceptionMiddleware
import logging
import sys
from typing import Callable

import orjson
import structlog
from fastapi import Request
from starlette.middleware.errors import ServerErrorMiddleware as ServerErrorMiddleware

shared_processors: list[Callable] = []
if sys.stderr.isatty():
    processors = shared_processors + [
        structlog.dev.ConsoleRenderer(),
    ]
else:
    processors = shared_processors + [
        structlog.processors.add_log_level,  # type: ignore[attr-defined]
        structlog.processors.TimeStamper(fmt="iso", utc=True),  # type: ignore[call-arg]
        structlog.processors.format_exc_info,
        structlog.contextvars.merge_contextvars,  # type: ignore[attr-defined]
        structlog.processors.JSONRenderer(orjson.dumps),  # type: ignore[call-arg]
    ]
structlog.configure(
    cache_logger_on_first_use=True,
    # wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=processors,
    # logger_factory=structlog.BytesLoggerFactory(),
)
logger = structlog.get_logger()


async def log_request(request: Request, e: Exception):
    logger.error("Error", exc_info=(type(e), e, e.__traceback__))  # , **request.scope)
    raise e


uvicorn = logging.getLogger("uvicorn.error")
uvicorn.disabled = True
