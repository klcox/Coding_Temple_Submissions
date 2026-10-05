from fastapi import Request
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)        


class DuplicateError(Exception):
    """Raised when creating a resource would violate a uniqueness constraint."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message) 


class AppValidationError(Exception):
    """Raised for domain-level validation failures (beyond Pydantic schema checks)."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message) 


class InternalError(Exception):
    """Raised for other, unhandled errors, such as internal server errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message) 


def JSON_error_response(error_type: str, message: str, status_code: int):
    """Helper function that takes a status_code, error_type, and error message so as to create a JSON response."""

    return JSONResponse(
        status_code = status_code,
        content = {
            "error_status": True,
            "error_type": error_type,
            "message": message,
            "status_code": status_code,
        }
    )

async def not_found_handler(request: Request, exc: NotFoundError):
    """Handles NotFoundError → 404 response."""

    return JSON_error_response("NotFoundError", exc.message, 404)    


async def duplicate_handler(request: Request, exc: DuplicateError):
    """Handles DuplicateError → 409 response."""

    return JSON_error_response("DuplicateError", exc.message, 409)


async def app_validation_handler(request: Request, exc: AppValidationError):
    """Handles AppValidationError → 422 response."""

    return JSON_error_response("AppValidationError", exc.message, 422)


async def internal_exception_handler(request: Request, exc: InternalError):
    """Catches any unhandled exception → 500 response."""

    return JSON_error_response("InternalError", exc.message, 500)