from fastapi import FastAPI

from erap.api.errors.exceptions import ApplicationError
from erap.api.errors.handlers import (
    application_error_handler,
    unexpected_error_handler,
)
from erap.api.health import router as health_router
from erap.api.middleware import RequestIDMiddleware
from erap.config.settings import get_settings
from erap.observability.logging import configure_logging

settings = get_settings()

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Cloud-neutral Enterprise RAG Agent Platform",
)

app.add_middleware(RequestIDMiddleware)

app.include_router(health_router)

app.add_exception_handler(
    ApplicationError,
    application_error_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_error_handler,
)