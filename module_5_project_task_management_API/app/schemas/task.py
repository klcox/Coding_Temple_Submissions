from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime


class TaskPriority(str, Enum):
    """Only allow these possibilities for a task's priority"""

    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    completed: bool = False
    
    
class TaskUpdate(BaseModel):
    """Schema for partially updating a task (PATCH)"""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: Optional[TaskPriority] = None
    completed: Optional[bool] = None


class TaskResponse(TaskCreate):
    """Schema for returning a task"""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)