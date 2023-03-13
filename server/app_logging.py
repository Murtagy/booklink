# from starlette.middleware.exceptions import ExceptionMiddleware as ExceptionMiddleware
import sys

import orjson
import structlog
from fastapi import Request
from starlette.middleware.errors import ServerErrorMiddleware as ServerErrorMiddleware

shared_processors = []
if sys.stderr.isatty():
    processors = shared_processors + [
        structlog.dev.ConsoleRenderer(),
    ]
else:
    processors = shared_processors + [
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.format_exc_info,
        structlog.contextvars.merge_contextvars,
        structlog.processors.JSONRenderer(serializer=orjson.dumps),
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
