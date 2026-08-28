from fastapi import FastAPI

from erap.api.health import router as health_router
from erap.config.settings import get_settings
from erap.observability.logging import configure_logging

settings = get_settings()

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Cloud-neutral Enterprise RAG Agent Platform",
)

app.include_router(health_router)