from fastapi import FastAPI
from app.routers import notes
from app.database import engine, Base
from app.models import note 

Base.metadata.create_all(bind=engine)  # For development only; creates tables if they do not already exist

app = FastAPI(
    title = "Notes API",
    description= "Sample project demonstrating the integration of FastAPI and SQLAlchemy",
    version = "0.1.0"
)

app.include_router(notes.router)

@app.get("/")
def root():
    return {"app": app.title, "docs": "/docs"}