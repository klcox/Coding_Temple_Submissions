from app.database import engine, Base
from app.models import student
from fastapi import FastAPI
from app.routers import students


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Student Records API",
    description = "A sample FastAPI demonstrating full CRUD operations.",
    version = "0.1.0"
)

app.include_router(students.router)

@app.get("/")
def root():
    return {"app": app.title, "docs": "/docs"}