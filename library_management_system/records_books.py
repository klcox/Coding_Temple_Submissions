from models import engine, Author, Book
from sqlalchemy.orm import Session


def list_all_authors():
    """Get all Authors currently in the database, ordered by name. Returns a list of tuples containing the Author ID, name, and bio ('N/A' if None); returns an empty list if no Authors exist."""
    
    with Session(engine) as session:

        authors = session.query(Author).order_by(Author.name).all()

        if not authors:            
            return []

        results = []

        for author in authors:
            bio = author.bio if author.bio is not None else "N/A"
            results.append(
                (author.id, author.name, bio)
            )
        return results


def list_all_books():
    """Get all Books currently in the database, ordered by title. Returns a list of tuples containing the Book ID, Book title, Author name(s), ISBN, year originally published (including era), and the number of available copies; returns an empty list if no Books exist."""
    
    with Session(engine) as session:

        books = session.query(Book).order_by(Book.title).all()

        if not books:            
            return []

        results = []
        
        for book in books:
            authors = ", ".join(sorted(author.name for author in book.authors))
            year = (f"{abs(book.year_published)} {book.era}")          
            results.append(
                (book.id, book.title, authors, book.isbn, year, book.available_copies)
            )

        return results
    

def add_author(name: str, bio: str = None):
    """Add a new Author. Returns None if successful."""

    # Data Validation - Name
    if name is None:
        raise ValueError("\nCannot add author. Name is required.")

    if type(name) != str:
        raise TypeError("\nCannot add author. Name must be a string.")

    if name.strip() == "":
        raise ValueError("\nCannot add author. Name cannot be empty.")

    name = name.strip().title()

    
    # Data Validation - Bio  
    if bio is not None:
        if type(bio) != str:
            raise TypeError("\nCannot add author. Bio must be a string.")

        if bio.strip() == "":
            raise ValueError("\nCannot add author. Bio can be None but cannot be an empty string.")

        bio = bio.strip()

    
    with Session(engine) as session:        
    
        # If no errors above persist, create Author and add to the database
        new_author = Author(name=name, bio=bio)

        try:
            session.add(new_author)
            session.commit()                      
        
        except Exception:
            session.rollback()
            print("\nError adding author to the database. Author not added. Please try again. ")
            raise

        print(f"\nAdded: {new_author}")        
            

def add_book(title: str, isbn: str, year_published: int, author_ids: list[int], available_copies: int = 1):
    """
    Add a new Book. Returns None if successful.
    author_ids is a list because Author and Books have a many-to-many relationship - authors can write many books, and books can have many authors.
    """

    # Data Validation - Title
    if title is None:
        raise ValueError("\nCannot add book. Title is required.")

    if type(title) != str:
        raise TypeError("\nCannot add book. Title must be a string.")

    if title.strip() == "":
        raise ValueError("\nCannot add book. Title cannot be empty.")

    title = title.strip()
    

    # Data Validation - ISBN
    if isbn is None:
        raise ValueError("\nCannot add book. ISBN is required.")

    if type(isbn) != str:
        raise TypeError("\nCannot add book. ISBN must be a string.")  

    isbn = isbn.strip()

    if not isbn.isdigit():
        raise ValueError("\nCannot add book. ISBN must contain only numbers.")

    if len(isbn) != 13:
        raise ValueError("\nCannot add book. ISBN must be exactly 13 characters.")
    

    # Data Validation - Year Published
    if year_published is None:
        raise ValueError("\nCannot add book. Year Published is required.")
    
    if type(year_published) != int:
        raise TypeError("\nCannot add book. Year Published must be an integer.")  

    # Era assigned based on Year Published 
    if year_published > 0:
        era = "CE"
    
    elif year_published < 0:
        era = "BCE"

    else:
        raise ValueError("\nCannot add book. Year Published cannot be 0.")


    # Data Validation - Available Copies
    if type(available_copies) != int:
        raise TypeError("\nCannot add book. Available Copies must be an integer.")

    if available_copies <= 0:
        raise ValueError("\nCannot add book. Available Copies cannot be 0 or a negative number.") 
    

    # Data Validation - Author ID(s)     
    if type(author_ids) != list:
        raise TypeError("\nCannot add book. Author IDs must be a list.")

    if not author_ids:  # Empty list case
        raise ValueError("\nCannot add book. At least one Author ID is required.")

    for id in author_ids:
        if type(id) != int:
            raise TypeError("\nCannot add book. All Author IDs must be integers.")   

    if len(author_ids) != len(set(author_ids)):
        raise ValueError("\nCannot add book. Duplicate Author IDs are not allowed.")     


    with Session(engine) as session:

        existing_book = session.query(Book).filter_by(isbn=isbn).first()


        # Check whether Book (ISBN) already exists
        if existing_book is not None:
            raise ValueError(f"\nCannot add book. ISBN {isbn} already exists in the database.")  

            
        # Check whether all Author IDs exist
        authors = []
        nonexistent_author_ids = []

        for author_id in author_ids:
            author = session.get(Author, author_id)            

            if author is None:
                nonexistent_author_ids.append(author_id)

            else:
                authors.append(author)

        if len(nonexistent_author_ids) == len(author_ids):
            raise ValueError("\nCannot add book. None of the Author IDs provided exist.")            

        elif len(nonexistent_author_ids) > 0:
            raise ValueError(f"\nCannot add book. One or more Author IDs do not exist: {nonexistent_author_ids}")
        

        # If no errors above persist, create Book and add to the database
        new_book = Book(title=title, isbn=isbn, year_published=year_published, era=era, available_copies=available_copies, authors=authors) 

        try:
            session.add(new_book)
            session.commit()                       
        
        except Exception:
            session.rollback()
            print("\nError adding book to the database. Book not added. Please try again. ")
            raise

        print(f"\nAdded: {new_book}")        
    

def delete_book(book_id: int):
    """Delete a Book if it is not currently checked out. Returns True if successful; returns False if there is an active checkout preventing the deletion."""

    # Data Validation - Book ID
    if book_id is None:
        raise ValueError("\nCannot delete book. Book ID is required.")

    if type(book_id) != int:
        raise TypeError("\nCannot delete book. Book ID must be an integer.")


    with Session(engine) as session:
        
        book = session.get(Book, book_id)

        # Check whether Book exists
        if book is None:
            raise ValueError(f"\nCannot delete book. Book ID {book_id} does not exist in the database.")


        # Check whether there are any active Checkouts
        for checkout in book.checkouts:
            if checkout.return_date is None:
                print("\nCannot delete book as it currently has an active checkout.")
                return False
            

        # If no errors above persist, delete the Book from the database
        try:
            session.delete(book)
            session.commit()            

        except Exception:
            session.rollback()
            print("\nError deleting book from the database. Book not deleted. Please try again.")
            raise

        print(f"\nDeleted book with ID {book_id} from the database.")
        return True