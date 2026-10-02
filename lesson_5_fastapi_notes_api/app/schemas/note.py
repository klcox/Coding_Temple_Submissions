from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class NoteCreate(BaseModel):
    """Schema for creating a note."""

    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    category: Optional[str] = Field(default=None, max_length=50)
    is_pinned: bool = False  # Default is False


class NoteResponse(NoteCreate):
    """Schema for returning a note."""

    id: int
    created_at: datetime

    model_config=ConfigDict(from_attributes=True)  # Allows Pydantic to read SQLAlchemy model attributes
