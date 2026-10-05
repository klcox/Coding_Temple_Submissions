from pydantic import BaseModel, Field, field_validator, ConfigDict


class UserCreate(BaseModel):    
    """Schema for creating a user."""

    username: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=7, max_length=200)
    password: str = Field(min_length=8, max_length=200)

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        """Validation for email address."""

        if "@" not in v:
            raise ValueError("Must be a valid email address (contains @)")
        return v


class UserResponse(BaseModel):
    """Schema for returning a user. Password is omitted."""

    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Schema for providing a JWT."""

    access_token: str
    token_type: str = "bearer"