import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    logger.info("Health check requested")
    return {"status": "healthy"}


@router.get("/ready")
async def readiness() -> dict[str, str]:
    logger.info("Readiness check requested")
    return {"status": "ready"}