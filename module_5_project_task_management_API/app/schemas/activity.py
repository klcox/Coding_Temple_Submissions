from pydantic import BaseModel, ConfigDict
from app.utils.enums import ActivityLogAction
from typing import Optional
from datetime import datetime


class ActivityLogCreate(BaseModel):
    """Schema for creating a user's activity log entry."""

    user_id: int
    task_id: int | None
    task_title: str
    action: ActivityLogAction
    changes: Optional[str] = None

    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": {                
                "user_id": 1,
                "task_id": 1,
                "task_title": "Buy Groceries",
                "action": "created",
                "changes": None
            }
        }
    )


class ActivityLogResponse(ActivityLogCreate):
    """Schema for returning a user's activity log entry."""

    id: int    
    timestamp: datetime      

    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": {                
                "user_id": 1,
                "task_id": 1,
                "task_title": "Buy Groceries",
                "action": "created",
                "changes": None,
                "id": 1,
                "timestamp": "2026-10-13T12:00:00"                
            }
        }
    )


class ActivityLogPaginationMeta(BaseModel):
    """Schema for activity log pagination metadata."""

    total: int    
    num_pages: int
    page: int
    limit: int    

    # Sample schema included as "meta" in the schema below


class ActivityLogPaginationResponse(BaseModel):
    """Schema for paginated activity log results"""

    data: list[ActivityLogResponse]
    meta: ActivityLogPaginationMeta     

    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": {                
                "data": [
                    {
                        "user_id": 1,
                        "task_id": 1,
                        "task_title": "Buy Groceries",
                        "action": "created",
                        "changes": None,
                        "id": 1,
                        "timestamp": "2026-10-13T12:00:00"
                    },
                    {
                        "user_id": 1,
                        "task_id": 2,
                        "task_title": "Finish Homework",
                        "action": "created",
                        "changes": None,
                        "id": 2,
                        "timestamp": "2026-10-13T12:30:00"
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