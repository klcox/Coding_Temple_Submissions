from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from typing import Optional


class Student(Base):

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    major: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    gpa: Mapped[Optional[float]] = mapped_column(nullable=True)