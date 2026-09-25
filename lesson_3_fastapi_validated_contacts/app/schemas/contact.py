from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ContactCategory(str, Enum):
    """Only allow these specific values for a contact's category."""

    personal = "personal"
    work = "work"
    family = "family"

class ContactCreate(BaseModel):
    """Schema for creating a new contact. Includes value restrictions for first_name, last_name, and (if provided) phone as well as custom validation for email."""

    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: str
    phone: Optional[str] = Field(default=None, min_length=10, max_length=15)
    category: ContactCategory

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        if "@" not in v:
            raise ValueError("must be a valid email address")
        return v

class ContactUpdate(BaseModel):
    """Schema for updating an existing contact. All fields are optional."""

    first_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email: Optional[str] = None
    phone: Optional[str] = Field(default=None, min_length=10, max_length=15)
    category: Optional[ContactCategory] = None

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        """Validation for email if provided."""

        if v is not None and "@" not in v:
            raise ValueError("must be a valid email address")
        return v

class ContactResponse(BaseModel):
    """Schema for returning a contact."""

    contact_id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    category: ContactCategory
    created_at: str