from fastapi import FastAPI
from app.database import Base, engine

from app.exceptions import NotFoundError, DuplicateError, AppValidationError, InternalError
from app.exceptions import not_found_handler, duplicate_handler, app_validation_handler, internal_exception_handler

from app.routers import students

app = FastAPI(title="Custom Errors API")

Base.metadata.create_all(bind=engine)

app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(DuplicateError, duplicate_handler)
app.add_exception_handler(AppValidationError, app_validation_handler)
app.add_exception_handler(InternalError, internal_exception_handler)

app.include_router(students.router)

@app.get("/")
def root():
    return {"app": app.title, "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
