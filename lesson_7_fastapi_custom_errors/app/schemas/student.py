# exercises/custom-errors/app/schemas/student.py
# L7 — Student schemas (same as L6)

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str
    major: Optional[str] = None
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("email must contain @")
        return v.lower()


class StudentResponse(StudentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
