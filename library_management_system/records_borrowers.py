from models import engine, Borrower, Checkout
from sqlalchemy.orm import Session
import re
from datetime import date


# Helper functions


def validate_borrower_email(email: str): 
    """Validation of a Borrower email address. If successful, returns the validated email address."""

    if email is None:
            raise ValueError("Cannot proceed. Email is required.")
        
    if type(email) != str:
        raise TypeError("Cannot proceed. Email must be a string.")
    
    if email.strip() == "":
        raise ValueError("Cannot proceed. Email cannot be empty.")  

    email = email.strip().lower() 


    email_pattern = r'[\w.+-]+@[\w-]+\.[\w.]+'       
    match = re.fullmatch(email_pattern, email)

    if not match:
        raise ValueError(f"Cannot proceed. The email address provided is not a valid email address.")   

    return email


def check_if_email_exists(email: str):  # Separated from validate_borrower_email due to different usage across two primary functions below
    """Check if the email address provided already belongs to another borrower in the database as email addresses must be unique. If cleared, returns the email address."""
    
    with Session(engine) as session:

        test_borrower = session.query(Borrower).filter_by(email_address=email).first() 

        if test_borrower is not None:
            raise ValueError(f"Cannot proceed. Email address {email} already exists for another borrower (ID: {test_borrower.id}) in the database.")
      
    return email


def normalize_borrower_phone(phone: str): 
    """Normalization of a Borrower phone number; occurs in add_borrower(), before adding the Borrower to the database. Returns the cleaned, normalized phone number."""

    phone = phone.strip()

    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.fullmatch(phone_pattern, phone)
    
    if not match:
        raise ValueError(f"Cannot proceed. The phone number provided is not a valid phone number.") 
       
   
    clean_num = re.sub(r'\D', '', phone)  # If a valid phone number, Step 1: normalize format by removing any non-digits
    new_num = f"{clean_num[:3]}-{clean_num[3:6]}-{clean_num[6:10]}"  # Step 2: reformat phone number for readability and consistency in the database


    phone = new_num
    return phone


def validate_borrower_id(borrower_id: int):
    """Validation of a Borrower ID. If successful, returns the validated Borrower ID."""

    if borrower_id is None:
        raise ValueError("Cannot proceed. Borrower ID is required.")

    if type(borrower_id) != int:
        raise TypeError("Cannot proceed. Borrower ID must be an integer.") 
    
    
    # Test to see if the ID exists in the database
    with Session(engine) as session:
    
        borrower = session.get(Borrower, borrower_id)

        if borrower is None:
            raise ValueError(f"Cannot proceed. Borrower ID {borrower_id} does not exist.")

    return borrower_id


# Primary functions


def add_borrower(name: str, email: str, phone: str = None):
    """Add a new Borrower. Returns the created Borrower object."""
        
    # Data Validation - Name
    if name is None:
        raise ValueError("Cannot add borrower. Name is required.")

    if type(name) != str:
        raise TypeError("Cannot add borrower. Name must be a string.")

    if name.strip() == "":
        raise ValueError("Cannot add borrower. Name cannot be empty.")   

    name = name.strip().title()


    # Data Validation - Email    
    email = validate_borrower_email(email)   
    email = check_if_email_exists(email)
   

    # Data Validation - Phone 
    if phone is not None:
        if type(phone) != str:
            raise TypeError("Cannot add borrower. Phone Number must be a string.")
    
        if phone.strip() == "":
            raise ValueError("Cannot add borrower. Phone Number can be None but cannot be an empty string.")
        
        phone = normalize_borrower_phone(phone)
            
    
    with Session(engine) as session:      
        
        # If no errors above persist, create Borrower and add to the database
        new_borrower = Borrower(name=name, email_address=email, phone=phone)

        try:
            session.add(new_borrower)
            session.commit()
            session.refresh(new_borrower)  # Populates the auto-generated id
            return new_borrower
        
        except Exception:
            session.rollback()
            print("Error adding borrower to the database. Borrower not added. Please try again. ")
            raise


def list_all_borrowers():
    """Get all Borrowers currently in the database, ordered by name. Returns a list of tuples containing the Borrower ID, name, and email address; returns an empty list if no Borrowers exist."""
    
    with Session(engine) as session:

        borrowers = session.query(Borrower).order_by(Borrower.name).all()

        if not borrowers:
            print("Currently, there are no borrowers in the database.")
            return []

        results = []
        
        for borrower in borrowers:            
            results.append((borrower.id, borrower.name, borrower.email_address))

        return results


def update_borrower_email(borrower_id: int, new_email: str):
    """Update a Borrower's email address. Returns the Borrower object."""

    # Data Validation - Borrower ID
    borrower_id = validate_borrower_id(borrower_id)

    # Data Validation - New Email Address
    new_email = validate_borrower_email(new_email)    
   

    with Session(engine) as session:
    
        borrower = session.get(Borrower, borrower_id)      
         
        if new_email == borrower.email_address:
            raise ValueError("Cannot update borrower email. The new email address provided is the same as the current email address on file.") 

        new_email = check_if_email_exists(new_email)
                   

        # If no errors above persist, update the Borrower email address
        borrower.email_address = new_email        
        
        try:            
            session.commit()
            session.refresh(borrower)  # Populates the auto-generated id
            return borrower
        
        except Exception:
            session.rollback()
            print("Error updating borrower email in the database. Borrower email address not updated. Please try again. ")
            raise


def get_checkouts_by_borrower(borrower_id: int):
    """Get a list of Checkout activity for the designated Borrower. Returns a list of tuples (sorted by due date) containing the Checkout ID, Book title, Checkout date, due date, return date, and whether returned Books were returned late; returns an empty list if the Borrower does not have any Checkout activity."""
  
    # Data Validation - Borrower ID
    borrower_id = validate_borrower_id(borrower_id)


    with Session(engine) as session:
    
        borrower = session.get(Borrower, borrower_id)       

        if not borrower.checkouts:
            print(f"Borrower with ID {borrower_id} does not have any checkout activity.")
            return []
        
        results = []
        
        for checkout in borrower.checkouts: 
            late_status = "Late" if checkout.return_date is not None and checkout.due_date < checkout.return_date else "On-Time"         
            results.append((checkout.id, checkout.book.title, checkout.checkout_date, checkout.due_date, checkout.return_date, late_status))

        sorted_results = sorted(results, key=lambda c: c.due_date)
        
        return sorted_results
    

def get_overdue_books():
    """Get a list of overdue Books. Returns a list of tuples (ordered by due date) containing the Checkout ID, Book title, Borrower ID, due date, and the number of days late; returns an empty list if no Books are overdue."""

    with Session(engine) as session:

        today = date.today()
        
        overdue_checkouts = session.query(Checkout).filter(Checkout.due_date < today, Checkout.return_date.is_(None)).order_by(Checkout.due_date).all()

        if not overdue_checkouts:
            print("No books currently overdue.")
            return []
        
        results = []

        for checkout in overdue_checkouts:            
            days_late = today - checkout.due_date
            results.append((checkout.id, checkout.book.title, checkout.borrower.id, checkout.due_date, days_late.days))

        return results
    

def delete_borrower(borrower_id: int):
    """Delete a Borrower if they do not currently have any active Checkouts. Returns True if successful; returns False if there is an active checkout preventing the deletion."""

    # Data Validation - Borrower ID
    borrower_id = validate_borrower_id(borrower_id)   
    

    with Session(engine) as session:
    
        borrower = session.get(Borrower, borrower_id)  

        for checkout in borrower.checkouts:
            if checkout.return_date is None:
                print(f"Cannot delete borrower as they currently have a book checked out.")
                return False

        # If no errors above persist, delete the Borrower from the database
        try:            
            session.delete(borrower)
            session.commit()
            print(f"Deleted borrower with ID {borrower_id} from the database.")
            return True
        
        except Exception:
            session.rollback()
            print("Error deleting borrower from the database. Borrower not deleted. Please try again. ")
            raise
        

       