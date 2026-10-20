from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utils.enums import ActivityLogAction
from sqlalchemy import Enum as SQLEnum, String, ForeignKey
from typing import Optional
from datetime import datetime
from sqlalchemy.sql import func


if TYPE_CHECKING:  # Conditional import for Pylance type-checking
    from app.models.user import User
    from app.models.task import Task


class ActivityLog(Base):
    """SQLAlchemy model for a user's activity log entry"""

    __tablename__ = "activity_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_title: Mapped[str] = mapped_column(nullable=False)  # Included in the event that a task is deleted and no longer accessible via ID
    action: Mapped[ActivityLogAction] = mapped_column(SQLEnum(ActivityLogAction), nullable=False)
    changes: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # Only applies to updates
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())    


    # Relationship to Users
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="activity_log")   


    # Relationship to Tasks
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"), nullable=True)  # Can be nullable in the event that a task is deleted
    task: Mapped["Task"] = relationship(back_populates="activity_log") 

