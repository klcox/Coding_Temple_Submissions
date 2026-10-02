from fastapi import APIRouter, Depends, HTTPException
from app.schemas.note import NoteCreate, NoteResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.note import Note
from typing import Optional


router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.post("/", response_model=NoteResponse, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """Create a new note in the database."""

    db_note = Note(**note.model_dump())      
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note  # Pydantic converts via from_attributes


@router.get("/", response_model=list[NoteResponse])
def list_notes(
    category: Optional[str] = None,
    is_pinned: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """List all notes, with optional filters for category and is_pinned"""

    query = db.query(Note)
    if category is not None:
        query = query.filter(Note.category == category)
    if is_pinned is not None:
        query = query.filter(Note.is_pinned == is_pinned)
    notes = query.all()

    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """Get a specific note by ID."""

    note = db.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    
    return note


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a specific note by ID."""

    note = db.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

    db.delete(note)
    db.commit()

    return {"message": f"Note {note_id} deleted successfully."}