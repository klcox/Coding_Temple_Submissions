from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating a user. Includes email validation ('@' required)"""
    
    username: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=7, max_length=100)
    password: str = Field(min_length=8, max_length=200)

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        """Validation for email address."""

        if "@" not in v:
            raise ValueError("Must be a valid email address (contains @)")
        return v


class UserUpdate(BaseModel):
    """Schema for partially updating a user (PATCH). Includes email validation ('@' required) if email is provided"""

    email: Optional[str] = Field(default=None, min_length=7, max_length=100)
    password: Optional[str] = Field(default=None, min_length=8, max_length=200)

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        """Validation for email address if provided."""

        if v is not None and "@" not in v:
            raise ValueError("Must be a valid email address (contains @)")
        return v


class UserResponse(BaseModel):
    """Schema for returning a user"""

    id: int    
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Schema for providing a JWT"""

    access_token: str
    token_type: str = "bearer"