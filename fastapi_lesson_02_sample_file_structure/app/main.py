from fastapi import FastAPI
from app.config import settings
from app.routers import recipes, ingredients

app = FastAPI(
    title=settings.app_name,
    description="A properly structured FastAPI application utilizing recipes and ingredients as example resources",
    version="0.1.0"
)

app.include_router(recipes.router)
app.include_router(ingredients.router)

@app.get("/")
def root():
    return {"app": settings.app_name, "docs": "/docs"}