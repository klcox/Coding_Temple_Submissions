from pydantic import BaseModel

class RecipeCreate(BaseModel):
    """Schema for creating a new recipe."""

    title: str
    cuisine: str
    prep_time_minutes: int
    servings: int

class RecipeResponse(BaseModel):
    """Schema for returning a recipe."""

    id: int
    title: str
    cuisine: str
    prep_time_minutes: int
    servings: int