from fastapi import APIRouter, HTTPException
from typing import Optional
from app.schemas.contact import ContactCategory, ContactCreate, ContactResponse, ContactUpdate
from datetime import datetime


router = APIRouter(
    prefix = "/contacts",
    tags = ["Contacts"]
)


contacts_list = [
    {
        "contact_id": 1,
        "first_name": "Terri",
        "last_name": "Cox",
        "email": "test@gmail.com",
        "phone": None,
        "category": "family",
        "created_at": "2026-09-25T12:00:00"
    },
    {
        "contact_id": 2,
        "first_name": "Susie",
        "last_name": "Carmichael",
        "email": "susie.c@test.com",
        "phone": "555-555-5555",
        "category": "personal",
        "created_at": "2026-09-25T12:30:00"
    }
]
next_id = 3


# GET Endpoints

@router.get("/", response_model=list[ContactResponse])
def list_contacts(category: Optional[ContactCategory] = None):
    """GET all contacts, with the option to filter by category. Returns a list of contact objects."""

    if category:
        return [c for c in contacts_list if c["category"] == category]
    return contacts_list

@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    """GET a specific contact. Returns the contact as a JSON object."""

    for contact in contacts_list:
        if contact["contact_id"] == contact_id:
            return contact
    raise HTTPException(status_code=404, detail=f"Contact {contact_id} not found.")


# POST Endpoints

@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate):
    """Create (POST) a new contact. Returns the created contact as a JSON object."""

    global next_id
    new_contact = {
        "contact_id": next_id, 
        **contact.model_dump(),
        "created_at": datetime.now().isoformat()  # isoformat converts datetime to a string
    }
    contacts_list.append(new_contact)
    next_id += 1
    return new_contact


# PATCH Endpoints

@router.patch("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, updates: ContactUpdate):
    """Update (PATCH) an existing contact. Returns the updated contact as a JSON object."""

    for contact in contacts_list:
        if contact["contact_id"] == contact_id:
            update_data = updates.model_dump(exclude_unset=True)
            contact.update(update_data)
            return contact
    raise HTTPException(status_code=404, detail="Contact not found.")
