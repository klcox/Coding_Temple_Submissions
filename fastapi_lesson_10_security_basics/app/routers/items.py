import re
from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator


router = APIRouter()


class ItemCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(default="", max_length=500)

    @field_validator("name", "description")
    @classmethod
    def sanitize_input(cls, value):
        """Sanitizes user input as a security measure."""

        value = value.strip()  # Strips extraneous white space

        value = re.sub(r"<[^>]*>", "", value)  # Removes HTML tags to prevent unauthorized scripts (XSS attacks)

        return value


items = [
    {
        "id": 1,
        "name": "Item_A",
        "description": "Sample item"
    },
    {
        "id": 2,
        "name": "Item_B",
        "description": "Sample item"
    },
    {
        "id": 3,
        "name": "Item_C",
        "description": "Sample item"
    }
]

next_id: int = 4


@router.get("/")
def list_items():
    """
    Returns all items.

    Security note: SQL injection prevention
    ----------------------------------------
    Normally, this function would query the database to retrieve all items (typically with optional filters) before returning the items.

    For example, a safe method of querying the database is to use a parameterized query such as the following:

        items = db.query(Item).filter(Item.name == name).all()

    This is safe because SQLAlchemy automatically parameterizes the query. It treats the user input as data, rather than as a direct part of the SQL code.

    In contrast, a query with raw SQL (non-parameterized), such as the following:

        result = db.execute(f"SELECT * FROM items WHERE name = '{name}'")
            
    is dangerous because it inserts the user input directly into the SQL code. This leaves the program vulnerable to SQL injection attacks, whereby an attacker submits input that contains malicious code to be used in SQL queries. For instance, an attacker could send name='; DROP TABLE users; -- and delete the entire database.

    For these reasons, it is a security best-practice to utilize parameterized queries only.

    Note: If raw SQL must be used (typically a rare occurrence), the query should be manually parameterized, such as the following:

        result = db.execute(text("SELECT * FROM items WHERE name = :name"), {"name": name})

    This is parameterized because it separates the variable storing the user input from the raw SQL code.
    """

    return items


@router.post("/")
def create_item(item: ItemCreate):
    """Creates an item. Input is sanitized by the schema validator."""

    global next_id

    new_item = {"id": next_id, **item.model_dump()}
    items.append(new_item)

    next_id += 1

    return new_item