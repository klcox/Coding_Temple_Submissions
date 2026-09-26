from fastapi import APIRouter, HTTPException, Path, Query
from app.schemas.book import BookGenre, BookSort, BookResponse
from typing import Optional


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# Sample data
books_list = [  
    {
        "book_id": 1,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genre": "fiction",
        "year": 1813,
        "available": True
    },
    {
        "book_id": 2,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": "fiction",
        "year": 1937,
        "available": False
    },
    {
        "book_id": 3,
        "title": "Educated",
        "author": "Tara Westover",
        "genre": "nonfiction",
        "year": 2018,
        "available": True
    },
    {
        "book_id": 4,
        "title": "Into the Wild",
        "author": "Jon Krakauer",
        "genre": "nonfiction",
        "year": 1996,
        "available": True
    },
    {
        "book_id": 5,
        "title": "The Immortal Life of Henrietta Lacks",
        "author": "Rebecca Skloot",
        "genre": "nonfiction",
        "year": 2010,
        "available": True
    },
    {
        "book_id": 6,
        "title": "Silent Spring",
        "author": "Rachel Carson",
        "genre": "science",
        "year": 1962,
        "available": False
    },
    {
        "book_id": 7,
        "title": "The Gene: An Intimate History",
        "author": "Siddhartha Mukherjee",
        "genre": "science",
        "year": 2016,
        "available": True
    },
    {
        "book_id": 8,
        "title": "Cosmos",
        "author": "Carl Sagan",
        "genre": "science",
        "year": 1980,
        "available": True
    },
    {
        "book_id": 9,
        "title": "Team of Rivals",
        "author": "Doris Kearns Goodwin",
        "genre": "history",
        "year": 2005,
        "available": False
    },
    
    {
        "book_id": 10,
        "title": "The Wright Brothers",
        "author": "David McCullough",
        "genre": "history",
        "year": 2015,
        "available": False
    }
]


@router.get("/", response_model=list[BookResponse])
def list_books(
    genre: Optional[BookGenre] = None,
    min_year: int = Query(default=1, gt=0),
    max_year: int = 2050,
    sort_by: BookSort = BookSort.book_id,
    search_title: Optional[str] = Query(default=None, min_length=1, max_length=70),
    search_author: Optional[str] = Query(default=None, min_length=1, max_length=70),
    search_available: Optional[bool] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=25, description="Max number of results")

):
    """List all books, with options for filtering, sorting, and pagination. Returns a list of book objects."""

    results = books_list.copy()


    # Apply filters
    if genre:  # If the user supplied the genre as a query parameter, select only the books that match this genre
        results = [b for b in results if b["genre"] == genre]

    results = [b for b in results if min_year <= b["year"] <= max_year]  # Select only the books that fall between the min_ and max_year (either defaults or user-supplied query parameters)

    if search_title:  # If the user supplied a query parameter to search by title, select only the books that contain the search content in the title
        results = [b for b in results if search_title.lower() in b["title"].lower()]

    if search_author:  # If the user supplied a query parameter to search by author, select only the books that contain the search content in the author name
        results = [b for b in results if search_author.lower() in b["author"].lower()]

    if search_available is not None:  # If the user supplied a query parameter to search by availability, select only the books that match the query parameter
        results = [b for b in results if search_available == b["available"]]


    # Sort results
    results.sort(key=lambda b: b[sort_by.value])  # Sort books by user-supplied query parameter; otherwise default is to sort by book title


    # Pagination    
    results = results[skip: skip + limit]  # Select only the books that fall between skip and limit (either defaults or user-supplied query parameters)


    return results


@router.get("/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int = Path(gt=0, description="Book ID must be greater than 0")):
    """Get a specific book by book_id. Returns the book as a JSON object."""

    for book in books_list:
        if book["book_id"] == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/genre/{genre}", response_model=list[BookResponse])
def get_books_by_genre(
    genre: BookGenre,
    sort_by: BookSort = BookSort.title
):
    """List all books from a specific genre, with the option to sort by book_id, title, author, or year. Returns a list of book objects."""

    results = [b for b in books_list if b["genre"] == genre]

    results.sort(key=lambda b: b[sort_by.value])

    return results