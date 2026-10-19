from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


# ==========
# EXCEPTIONS
# ==========


class AppException(Exception):
    """Base exception class for the application."""

    def __init__(self, detail: str, status_code: int, headers = None):
        self.detail = detail
        self.status_code = status_code
        self.headers = headers

class BadRequestException(AppException):
    """Raised when a request is missing required fields or when a business rule is violated, e.g. an end_date earlier than a start_date."""

    def __init__(self, detail: str):
        super().__init__(
            detail = detail,
            status_code = 400            
        )

class UnauthorizedException(AppException):
    """Raised when a token or user cannot be authenticated."""

    def __init__(self, detail: str):
        super().__init__(
            detail = detail,
            status_code = 401,
            headers = {"WWW-Authenticate": "Bearer"}
        )

class ForbiddenException(AppException):
    """Raised when there are insufficient permissions (i.e. a user is authenticated but does not have permission to perform the action)."""

    def __init__(self, detail: str = "You do not have permission to perform this action."):
        super().__init__(
            detail = detail,
            status_code = 403
        )

class NotFoundException(AppException):
    """Raised when a requested resource is not found/does not exist."""

    def __init__(self, resource: str, resource_identifier: str):
        super().__init__(
            detail = f"{resource} with {resource_identifier} not found.",
            status_code = 404            
        )

class DuplicateException(AppException):
    """Raised when creating a resource would violate a uniqueness constraint."""

    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            detail = f"{resource} with {field} '{value}' already exists.", 
            status_code = 409
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
            "error_type": type(exc).__name__,
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
        headers = exc.headers
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