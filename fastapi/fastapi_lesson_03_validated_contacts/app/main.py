from fastapi import FastAPI
from app.routers import contacts

app = FastAPI(
    title = "Contact Book API",
    description = "A sample Fast API project demonstrating validated contacts.",
    version = "0.1.0"
)

app.include_router(contacts.router)

@app.get("/")
def root():
    return {"app": app.title}