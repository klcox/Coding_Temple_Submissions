from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ItemCreate(BaseModel):
    """Schema for creating an item."""

    name: str = Field(min_length=1, max_length=100, description="Item name, must be between 1-100 characters")
    description: Optional[str] = Field(default=None, max_length=500, description="Item description (optional), max length of 500 characters")
    price: float = Field(gt=0, description="Item price in USD, must be greater than zero")
    category: str = Field(min_length=1, max_length=50, description="Item category, e.g. 'electronics', 'accessories', must be between 1-50 characters")

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "name": "Charging Cable",
                "description": "For Android phones, supports USB and USB-C",
                "price": 12.99,
                "category": "accessories"            
            }
        }        
    )    


class ItemResponse(ItemCreate):
    """Schema returned to clients — includes server-assigned id; all other attributes inherited from ItemCreate."""

    id: int

    model_config = ConfigDict(
        from_attributes = True,        
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Charging Cable",
                "description": "For Android phones, supports USB and USB-C",
                "price": 12.99,
                "category": "accessories"            
            }
        }        
    ) 