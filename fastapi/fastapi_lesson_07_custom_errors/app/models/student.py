# exercises/custom-errors/app/models/student.py
# L7 — Student model (same as L6)

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.database import Base


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    major: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    gpa: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
