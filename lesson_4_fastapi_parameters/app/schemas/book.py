from pydantic import BaseModel, Field
from enum import Enum

class BookGenre(str, Enum):
    """Options for book genre."""

    fiction = "fiction"
    nonfiction = "nonfiction"
    science = "science"
    history = "history"

class BookSort(str, Enum):
    """Options for sorting books."""

    book_id = "book_id"
    title = "title"
    author = "author"
    year = "year"

class BookResponse(BaseModel):
    """Schema for returning a book."""

    book_id: int
    title: str 
    author: str 
    genre: BookGenre
    year: int = Field(gt=0)
    available: bool = True