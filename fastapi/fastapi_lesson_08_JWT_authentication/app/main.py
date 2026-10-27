from app.database import Base, engine
from fastapi import FastAPI
from app.utils.exceptions import AppException, app_exception_handler
from app.routers import auth


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Sample JWT Authentication App",
    description= "A simple FastAPI application demonstrating JWT authentication concepts.",
    version = "0.1.0"
)


app.add_exception_handler(AppException, app_exception_handler)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"app": app.title, "docs": "/docs"}