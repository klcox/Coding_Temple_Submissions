from fastapi import FastAPI
from app.routers import books

app = FastAPI(
    title = "Sample Library API",
    description="A Fast API project demonstrating path and query parameters.",
    version = "0.1.0"
)

app.include_router(books.router)

@app.get("/")
def root():
    return {"app": app.title, "docs": "/docs"}