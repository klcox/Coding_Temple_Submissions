from pydantic import BaseModel, ConfigDict
from app.enums import ActivityLogAction
from datetime import datetime


class ActivityLogCreate(BaseModel):
    """Schema for creating a user's activity log entry."""

    user_id: int
    task_id: int | None
    task_title: str
    action: ActivityLogAction        

    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": {                
                "user_id": 1,
                "task_id": 1,
                "task_title": "Buy Groceries",
                "action": "created"                               
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
                "id": 1,
                "timestamp": "2026-10-13T12:00:00"                
            }
        }
    )