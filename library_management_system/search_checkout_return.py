from models import engine, Author, Book, Borrower, Checkout
from sqlalchemy.orm import Session
from datetime import date, timedelta


def list_available_books():
    """Searches for all Books with copies available for checkout. Returns a list of tuples containing the Book ID, Book title, and Author name(s); returns an empty list if no matching Books are found."""

    with Session(engine) as session:
    
        books = session.query(Book).filter(Book.available_copies >= 1).order_by(Book.title).all()

        if not books:            
            return []
        
        results = []

        for book in books:
            authors = ", ".join(author.name for author in book.authors) 
            results.append((book.id, book.title, authors))

        return results


def find_books_by_author(author_name: str):
    """Searches for Books where the Author name contains author_name (e.g. 'Smith'), case-insensitive. Returns a list of tuples containing the Book ID, Author name(s), and Book title; returns an empty list if no matching Authors are found."""

    # Data Validation - Author Name
    if author_name is None:
        raise ValueError("Cannot search books. Author Name is required.")

    if type(author_name) != str:
        raise TypeError("Cannot search books. Author Name must be a string.")

    if author_name.strip() == "":
        raise ValueError("Cannot search books. Author Name cannot be empty.")

    author_name = author_name.strip()

    
    with Session(engine) as session:

        authors = session.query(Author).filter(Author.name.ilike(f"%{author_name}%")).order_by(Author.name).all()

        if not authors:            
            return []

        results = []
        seen_books = set()  # Prevents the same book from being displayed twice if there are multiple authors whose name matches author_name

        for author in authors:
            for book in author.books:
                if book.id not in seen_books:
                    author_names = ", ".join(author.name for author in book.authors)
                    results.append((book.id, author_names, book.title))
                    seen_books.add(book.id)

        return results
        

def find_books_by_keyword(keyword: str):
    """Searches for Books where the title contains keyword, case-insensitive. Returns a list of tuples containing the Book ID, Book title, and Author name(s); returns an empty list if no matching Books are found."""

    # Data Validation - Keyword
    if keyword is None:
        raise ValueError("Cannot search books. Keyword is required.")

    if type(keyword) != str:
        raise TypeError("Cannot search books. Keyword must be a string.")

    if keyword.strip() == "":
        raise ValueError("Cannot search books. Keyword cannot be empty.")

    keyword = keyword.strip()

    
    with Session(engine) as session:

        books = session.query(Book).filter(Book.title.ilike(f"%{keyword}%")).order_by(Book.title).all()

        if not books:            
            return []

        results = []

        for book in books:
            authors = ", ".join(author.name for author in book.authors) 
            results.append((book.id, book.title, authors))

        return results


def find_books_by_era(era: str):
    """Searches for books from the designated era. Returns a list of tuples containing the book ID, book title, and author name(s); returns an empty list if no matching books are found."""

    # Data Validation - Era
    if era is None:
        raise ValueError("Cannot search books. Era is required.")

    if type(era) != str:
        raise TypeError("Cannot search books. Era must be a string.")

    if era.strip() == "":
        raise ValueError("Cannot search books. Era cannot be empty.")

    era = era.strip().upper()

    if era not in ("BCE", "CE"):
        raise ValueError("Cannot search books. Era must be either 'BCE' or 'CE'.")

    
    with Session(engine) as session:

        books = session.query(Book).filter_by(era=era).order_by(Book.title).all()
        
        if not books:            
            return []

        results = []

        for book in books:
            authors = ", ".join(author.name for author in book.authors) 
            results.append((book.id, book.title, authors))

        return results    


def checkout_book(book_id: int, borrower_id: int, checkout_date: date = None):
    """Check out a book. Reduces the number of available copies by 1. Returns None if successful."""

    # Data Validation - Book ID
    if book_id is None:
        raise ValueError("Cannot create checkout. Book ID is required.")

    if type(book_id) != int:
        raise TypeError("Cannot create checkout. Book ID must be an integer.")


    # Data Validation - Borrower ID
    if borrower_id is None:
        raise ValueError("Cannot create checkout. Borrower ID is required.")

    if type(borrower_id) != int:
        raise TypeError("Cannot create checkout. Borrower ID must be an integer.")
    

    # Data Validation - Checkout Date
    today = date.today()

    if checkout_date is None:
        checkout_date = today

    if type(checkout_date) != date:
        raise TypeError("Cannot create checkout. Checkout Date must be a date.")

    if checkout_date > today:
        raise ValueError("Cannot create checkout. Checkout Date cannot be in the future.")

    two_days_ago = today - timedelta(days=2)
    if checkout_date < two_days_ago:
        raise ValueError("Cannot create checkout. Checkout Date cannot be more than (2) days ago.")


    with Session(engine) as session:

        # Check if Book exists and is available for checkout
        book = session.get(Book, book_id)

        if book is None:
            raise ValueError(f"Cannot create checkout. Book ID {book_id} does not exist.")

        if book.available_copies <= 0:
            raise ValueError(f"Cannot create checkout. Book ID {book_id} is not available for checkout.")  
          
    
        # Check if Borrower exists
        borrower = session.get(Borrower, borrower_id)

        if borrower is None:
            raise ValueError(f"Cannot create checkout. Borrower ID {borrower_id} does not exist.")
        

        # If no errors above persist, create Checkout and add to the database
        due_date = checkout_date + timedelta(days=14)  # Standard checkout period of 2 weeks

        new_checkout = Checkout(book=book, borrower=borrower, checkout_date=checkout_date, due_date=due_date)
        book.available_copies -= 1
        
        try:
            session.add(new_checkout)
            session.commit()        
        
        except Exception:
            session.rollback()
            print("Error adding checkout to the database. Book not checked out. Please try again. ")
            raise   

        print(f"Checkout confirmed. Checkout ID: {new_checkout.id}, Due Date: {new_checkout.due_date}")


def return_book(checkout_id: int):
    """Return a book. Sets return_date to today and adds 1 to the available copies. Returns True if the return is successful; returns False if the return cannot be completed as the book was already returned."""

    # Data Validation - Checkout ID
    if checkout_id is None:
        raise ValueError("Cannot return book. Checkout ID is required.")

    if type(checkout_id) != int:
        raise TypeError("Cannot return book. Checkout ID must be an integer.")    


    with Session(engine) as session:

        today = date.today()
    
        checkout = session.get(Checkout, checkout_id)

        if checkout is None:
            raise ValueError(f"Cannot return book. Checkout ID {checkout_id} does not exist.")        

        if checkout.return_date is not None:
            print(f"Cannot return book. '{checkout.book.title}' (Checkout ID:{checkout_id}) was returned on {checkout.return_date}.")
            return False


        # If no errors above persist, update the return date and the available copies             
        checkout.return_date = today
        checkout.book.available_copies += 1  

        try:       
            session.commit()            

        except Exception:
            session.rollback()
            print("Error returning book in the database. Book not returned. Please try again. ")
            raise 

        print(f"Book return confirmed for Checkout ID {checkout_id}.")
        
        if checkout.due_date < today: 
            print("**Note: Your book was returned after the scheduled due date. Late fees may apply.**")
            
        return True      