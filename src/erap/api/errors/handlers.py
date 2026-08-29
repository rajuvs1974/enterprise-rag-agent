import logging
from typing import cast

from fastapi import Request
from fastapi.responses import JSONResponse

from erap.api.errors.exceptions import ApplicationError
from erap.api.errors.models import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


async def application_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    application_error = cast(ApplicationError, exc)

    request_id = getattr(request.state, "request_id", "unknown")

    logger.warning(
        "Application error",
        extra={
            "request_id": request_id,
            "error_code": application_error.code,
        },
    )

    error_detail = ErrorDetail(
        code=application_error.code,
        message=application_error.message,
        request_id=request_id,
    )

    response = ErrorResponse(error=error_detail)

    return JSONResponse(
        status_code=400,
        content=response.model_dump(),
    )


async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")

    logger.exception(
        "Unexpected application error",
        extra={"request_id": request_id},
    )

    error_detail = ErrorDetail(
        code="INTERNAL_ERROR",
        message="An unexpected error occurred",
        request_id=request_id,
    )

    response = ErrorResponse(error=error_detail)

    return JSONResponse(
        status_code=500,
        content=response.model_dump(),
    )