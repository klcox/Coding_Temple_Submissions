from fastapi.responses import JSONResponse
from fastapi import Request


class AppException(Exception):
    """Base exception for the application."""

    def __init__(self, detail: str, status_code: int, headers=None):
        self.detail = detail
        self.status_code = status_code
        self.headers = headers


class InvalidAuthError(AppException):
    """Raised when a token or user cannot be authenticated."""

    def __init__(self, detail: str):
        super().__init__(
            detail = detail,
            status_code = 401,
            headers = {"WWW-Authenticate": "Bearer"}
        )        


class DuplicateError(AppException):
    """Raised when creating a resource would violate a uniqueness constraint."""

    def __init__(self, detail: str):
        super().__init__(
            detail = detail,
            status_code = 409
        )


class InternalError(AppException):
    """Raised for other, unhandled errors, such as internal server errors."""

    def __init__(self, detail: str):
        super().__init__(
            detail = detail,
            status_code = 500
        )


def JSON_error_response(error_type: str, detail: str, status_code: int, headers=None):
    """Helper function that creates a JSON response."""    

    return JSONResponse(
        status_code = status_code,
        content = {
            "error_status": True,
            "error_type": error_type,
            "detail": detail,
            "status_code": status_code                
        },
        headers = headers
    )
 

async def app_exception_handler(request: Request, exc: AppException):
    """Converts AppException subclasses to JSON responses."""

    return JSON_error_response(type(exc).__name__, exc.detail, exc.status_code, exc.headers)