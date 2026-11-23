from datetime import datetime, timezone
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions.custom_exceptions import AppException


def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "data": None,
            "error": exc.__class__.__name__,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append(f"{field}: {error['msg']}" if field else error["msg"])

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error: " + "; ".join(errors),
            "data": None,
            "error": "RequestValidationError",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
