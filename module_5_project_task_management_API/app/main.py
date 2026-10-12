from app.database import engine, Base
from app.models.task import Task
from app.models.user import User

from fastapi import FastAPI
from app.config import settings
from textwrap import dedent

from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from utils.exceptions import AppException, app_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError

from app.routers import auth, users, tasks


Base.metadata.create_all(bind=engine)  # Creates database tables if they do not already exist


# ========
# APP INFO
# ========


openapi_tags = [  # Assists in organizing routers in the documentation
    {
        "name": "Authentication", 
        "description": "Register a new user, validate credentials, and log-in"
    },
    {
        "name": "Users", 
        "description": "User profile management"
    },
    {
        "name": "Tasks", 
        "description": "Create and manage tasks"
    }
]

app = FastAPI(  # App info; appears at the top of the documentation
    title = settings.app_name,
    description = dedent("""
        A task management API built with FastAPI.

        ## Features
        - User registration and JWT authentication
        - CORS Middleware configuration
        - Rate limiting
        - Full CRUD for tasks, including filtering and pagination
        - Background task processing
        - Validation and error handling
        - An AI-ready endpoint
        - Pytest testing

        ## Authentication
        Most endpoints require a Bearer token. In the documentation:
        - Register at: `/auth/register'
        - Next, enter your username and password at `/auth/token` **(Note the access token received in the response.)**

        Then, for endpoints that require authentication:
        - Click the lock icon at the far-right of the endpoint
        - Paste the access token and click 'Authorize'
        - Click 'Try it out' and 'Execute' on the endpoints to test and view the responses
    """),
    version = "1.0.0",
    openapi_tags = openapi_tags,
    contact = {
        "name": "Kelly Cox", 
        "email": "example_email@test.com"
    },
    license_info = {
        "name": "MIT License",
        "url": "https://opensource.org/license/mit/"
    }
)


# ==========
# MIDDLEWARE
# ==========


app.add_middleware(  # Controls which websites are allowed to make requests to the API
    CORSMiddleware,
    allow_origins = [
        "http://localhost:3000",
        "http://localhost:8501"
    ],
    allow_credentials = True,
    allow_methods = ["GET", "POST", "PATCH", "DELETE"],
    allow_headers = ["Authorization", "Content-Type"]
)


# =============
# RATE LIMITING
# =============


limiter = Limiter(key_func=get_remote_address)  # Establishes rate limiter. Limits set in routers.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ==================
# EXCEPTION HANDLERS
# ==================


app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# =======
# ROUTERS
# =======


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)


# ====
# ROOT
# ====


@app.get("/")
def root():
    return {"app": app.title, "docs": "/docs"}


# ===================
# RUNNING THE PROGRAM
# ===================


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)