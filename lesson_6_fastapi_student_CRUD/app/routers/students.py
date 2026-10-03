from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.student import StudentCreate, StudentUpdate, StudentPatch, StudentResponse
from app.models.student import Student
from sqlalchemy.exc import IntegrityError 
from typing import Optional


router = APIRouter(
    prefix = "/students",
    tags = ["Students"]
)


def get_student_or_404(db: Session, student_id: int):
    """Helper function - Gets a student by ID or raises a 404 error if the student is not found."""

    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    return student


# CREATE


@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student. Raises a 409 error if the email address already exists in the database."""

    new_student = Student(**student.model_dump())

    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

    except IntegrityError:  # Catches duplicate email addresses
        db.rollback()
        raise HTTPException(status_code=409, detail=f"A student with email address {student.email} already exists.")

    except Exception:  # Catches unexpected errors encountered during database transaction
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred. New student was not created.")

    return new_student


# READ


@router.get("/", response_model=list[StudentResponse])
def list_students(
    major: Optional[str] = Query(default=None, max_length=100, description="Filter by major"),
    min_gpa: Optional[float] = Query(default=None, ge=0.0, le=4.0, description="Filter by minimum GPA"),
    db: Session = Depends(get_db)
):
    """Get a list of all students, with optional filtering by major and/or min_gpa."""

    query = db.query(Student)

    if major is not None:
        query = query.filter(Student.major.ilike(f"%{major}%"))

    if min_gpa is not None:
        query = query.filter(Student.gpa >= min_gpa)

    students = query.all()

    return students

@router.get("/{student_id}", response_model=StudentResponse)
def get_student_by_id(student_id: int = Path(gt=0, description="Student ID must be greater than 0"), db: Session = Depends(get_db)):
    """Get a specific student by ID."""

    return get_student_or_404(db, student_id)


# UPDATE


@router.put("/{student_id}", response_model=StudentResponse)
def replace_student(
    student_data: StudentUpdate, 
    student_id: int = Path(gt=0, description="Student ID must be greater than 0"),     
    db: Session = Depends(get_db)
):
    """Fully replace a student record (all fields required)."""

    student = get_student_or_404(db, student_id)    

    try:    
        for field, value in student_data.model_dump().items():
            setattr(student, field, value)

        db.commit()
        db.refresh(student)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"A student with email address {student_data.email} already exists.")

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Record for Student {student_id} was not updated.")

    return student
    
@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(
    student_data: StudentPatch, 
    student_id: int = Path(gt=0, description="Student ID must be greater than 0"),     
    db: Session = Depends(get_db)
):
    """Partially update a student record (only the fields sent by the client are changed)."""

    student = get_student_or_404(db, student_id) 

    update_data = {
        k: v
        for k, v in student_data.model_dump(exclude_unset=True).items()
        if v is not None or k in {"major", "gpa"}
    }

    try:
        for field, value in update_data.items():
            setattr(student, field, value)

        db.commit()
        db.refresh(student)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"A student with email address {student_data.email} already exists.")
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Record for Student {student_id} was not updated.")

    return student


# DELETE


@router.delete("/{student_id}")
def delete_student(student_id: int = Path(gt=0, description="Student ID must be greater than 0"), db: Session = Depends(get_db)):
    """Delete a specific student by ID."""

    student = get_student_or_404(db, student_id)

    try:
        db.delete(student)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Record for Student {student_id} was not deleted.")

    return {"message": f"Student record {student_id} deleted successfully."}        