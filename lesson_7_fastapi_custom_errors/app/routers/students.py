from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.student import StudentCreate, StudentResponse
from app.models.student import Student
from app.database import get_db

from sqlalchemy.exc import IntegrityError
from app.exceptions import NotFoundError, DuplicateError, InternalError

router = APIRouter(
    prefix = "/students",
    tags = ["Students"]
)


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Creates a student. Raises DuplicateError (not HTTPException) if email taken.    
    """

    new_student = Student(**student.model_dump())

    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

    except IntegrityError:
        db.rollback()
        raise DuplicateError(f"Cannot create student. Email address {student.email} already exists in the database.")

    except Exception:
        db.rollback()
        raise InternalError("Student not created. An internal server error occurred.")

    return new_student


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Gets a student. Raises NotFoundError if not found.    
    """

    student = db.get(Student, student_id)

    if not student:
        raise NotFoundError(f"Student {student_id} not found.")

    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Deletes a student. Raises NotFoundError if not found."""

    student = db.get(Student, student_id)
    
    if not student:
        raise NotFoundError(f"Cannot delete student. Student {student_id} not found.")

    try:
        db.delete(student)
        db.commit()
    
    except Exception:
        db.rollback()
        raise InternalError(f"Student {student_id} not deleted. An internal server error occurred.")

    return {"message": f"Student {student_id} deleted successfully."}