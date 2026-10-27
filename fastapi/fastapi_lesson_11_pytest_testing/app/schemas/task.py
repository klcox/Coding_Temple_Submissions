# exercises/test-suite/app/schemas/task.py
# L11 — Task schemas (already complete — this is what you're testing)

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = False


class TaskPatch(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
