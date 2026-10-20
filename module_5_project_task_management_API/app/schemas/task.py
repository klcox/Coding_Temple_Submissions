from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.utils.enums import TaskPriority
from datetime import datetime


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, min_length=1, max_length=2000)
    priority: TaskPriority = Field(default=TaskPriority.medium)    

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "title": "Buy Groceries",
                "description": "Apples, bananas, eggs, bread",
                "priority": "medium"                
            }
        }
    )
    
    
class TaskUpdate(BaseModel):
    """Schema for partially updating a task (PATCH)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, min_length=1, max_length=2000)
    priority: Optional[TaskPriority] = None
    completed: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {                                
                "completed": True                
            }
        }
    )


class TaskResponse(TaskCreate):
    """Schema for returning a task."""

    completed: bool
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": { 
                "title": "Buy Groceries",
                "description": "Apples, bananas, eggs, bread",
                "priority": "medium",
                "completed": False,               
                "id": 1,
                "user_id": 1,
                "created_at": "2026-10-13T12:00:00",
                "updated_at": "2026-10-13T12:00:00"             
            }
        }    
    )


class TaskPaginationMeta(BaseModel):
    """Schema for task pagination metadata."""

    total: int    
    num_pages: int
    page: int
    limit: int    

    # Sample schema included as "meta" in the schema below


class TaskPaginationResponse(BaseModel):
    """Schema for paginated task results."""

    data: list[TaskResponse]
    meta: TaskPaginationMeta     

    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": {                
                "data": [
                    {
                        "title": "Buy Groceries",
                        "description": "Apples, bananas, eggs, bread",
                        "priority": "medium",
                        "completed": False,               
                        "id": 1,
                        "user_id": 1,
                        "created_at": "2026-10-13T12:00:00",
                        "updated_at": "2026-10-13T12:00:00" 
                    },
                    {
                        "title": "Finish Homework",                        
                        "priority": "high",
                        "completed": False,               
                        "id": 2,
                        "user_id": 1,
                        "created_at": "2026-10-13T12:30:00",
                        "updated_at": "2026-10-13T12:30:00" 
                    }
                ],
                "meta": {
                    "total": 2,
                    "num_pages": 1,
                    "page": 1,
                    "limit": 10
                }              
            }
        }
    )