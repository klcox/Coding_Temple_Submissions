from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


class StudentCreate(BaseModel):
    """Schema for creating a student, with email validation ('@' required) - POST"""

    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=7, max_length=200)
    major: Optional[str] = Field(default=None, max_length=100)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        """Validation for email address."""

        if "@" not in v:
            raise ValueError("Must be a valid email address (contains @)")
        return v


class StudentUpdate(BaseModel):
    """Schema for fully updating (replacing) a student - PUT"""

    name: str = Field(max_length=100)
    email: str = Field(max_length=200)
    major: Optional[str] = Field(default=None, max_length=100)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        """Validation for email address."""

        if "@" not in v:
            raise ValueError("Must be a valid email address (contains @)")
        return v


class StudentPatch(BaseModel):
    """Schema for partially updating a student - PATCH"""

    name: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=200)
    major: Optional[str] = Field(default=None, max_length=100)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        """Validation for email address if provided."""

        if v is not None and "@" not in v:
            raise ValueError("Must be a valid email address (contains @)")
        return v


class StudentResponse(StudentCreate):
    """Schema for returning a student - GET and database queries"""

    id: int

    model_config = ConfigDict(from_attributes=True)