from enum import Enum


class TaskPriority(str, Enum):
    """Only allow these possibilities for a task's priority"""

    urgent = "urgent"
    high = "high"
    medium = "medium"
    low = "low"


class TaskSort(str, Enum):
    """Options for sorting tasks."""

    created_at = "created_at"
    title = "title"    
    completed = "completed"
    priority = "priority"


class TaskSortOrder(str, Enum):
    """Options for ordering sort results."""

    asc = "asc"
    desc = "desc"


class ActivityLogAction(str, Enum):
    """Options for activity log actions."""

    created = "created"
    updated = "updated"
    deleted = "deleted"