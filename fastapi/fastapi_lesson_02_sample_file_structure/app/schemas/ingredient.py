from pydantic import BaseModel

class IngredientCreate(BaseModel):
    """Schema for creating a new ingredient."""

    name: str
    category: str
    

class IngredientResponse(BaseModel):
    """Schema for returning an ingredient."""

    id: int
    name: str
    category: str