from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


# ==========
# EXCEPTIONS
# ==========


class AppException(Exception):
    """Base exception class for the application."""

    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code

class NotFoundException(AppException):
    """Raised when a requested resource is not found/does not exist."""

    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            detail = f"{resource} with ID {resource_id} not found.",
            status_code = 404            
        )

class DuplicateException(AppException):
    """Raised when creating a resource would violate a uniqueness constraint."""

    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            detail = f"{resource} with {field} '{value}' already exists.", 
            status_code = 409
        )

class UnauthorizedException(AppException):
    """Raised when authentication is required."""

    def __init__(self, detail: str = "Authentication required."):
        super().__init__(
            detail = detail,
            status_code = 401
        )

class InternalError(AppException):
    """Raised when a database action such as POST, PATCH, or DELETE could not be performed due to a server/database error."""

    def __init__(self, detail: str):
        super().__init__(
            detail = "An internal server error occurred. " + detail, 
            status_code = 500
        )        


# ========
# HANDLERS
# ========


async def app_exception_handler(request: Request, exc: AppException):
    """Convert all AppException classes to JSON responses."""

    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "error_status": True,            
            "detail": exc.detail,
            "status_code": exc.status_code,
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Simplify Pydantic validation error formatting."""

    errors = []

    for error in exc.errors():
        errors.append({
            "field": "->".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code = 422,
        content = {
            "error_status": True,            
            "detail": "Validation failed",
            "errors": errors
        }
    )