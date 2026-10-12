from enum import Enum


class TaskPriority(str, Enum):
    """Only allow these possibilities for a task's priority"""

    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"