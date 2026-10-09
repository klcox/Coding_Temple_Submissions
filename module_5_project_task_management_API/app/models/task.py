from enum import Enum
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from typing import Optional
from datetime import datetime
from sqlalchemy.sql import func


class TaskPriority(str, Enum):
    """Only allow these possibilities for a task's priority"""

    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class Task(Base):
    """SQLAlchemy model for a task"""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True, default=None)
    priority: Mapped[TaskPriority] = mapped_column(SQLEnum(TaskPriority), nullable=False, default=TaskPriority.medium)
    completed: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())  # server_default sets the timestamp when the table row is created; onupdate updates the timestamp when the row is updated

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # Relationship to Users
    user: Mapped["User"] = relationship(back_populates="tasks")    