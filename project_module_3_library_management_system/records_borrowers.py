from models import engine, Borrower, Checkout
from sqlalchemy.orm import Session
import re
from datetime import date


# Helper functions


def validate_borrower_id(borrower_id: int):
    """Validates a Borrower ID. If successful, returns the validated Borrower ID."""

    if borrower_id is None:
        raise ValueError("\nCannot proceed. Borrower ID is required.")

    if type(borrower_id) != int:
        raise TypeError("\nCannot proceed. Borrower ID must be an integer.")  
     
    return borrower_id


def validate_borrower_email(email: str): 
    """Validates a Borrower email address. If successful, returns the validated email address."""

    if email is None:
            raise ValueError("\nCannot proceed. Email is required.")
        
    if type(email) != str:
        raise TypeError("\nCannot proceed. Email must be a string.")
    
    if email.strip() == "":
        raise ValueError("\nCannot proceed. Email cannot be empty.")  

    email = email.strip().lower() 


    email_pattern = r'[\w.+-]+@[\w-]+\.[\w.]+'       
    match = re.fullmatch(email_pattern, email)

    if not match:
        raise ValueError(f"\nCannot proceed. The email address provided is not a valid email address.")   

    return email


def check_if_borrower_id_exists(session, borrower_id: int):  # Separated from validate_borrower_id() so as to prevent multiple sessions from being opened in the related functions below
    """Check whether the Borrower ID exists in the database so as to locate the borrower. If cleared, returns the Borrower object."""  

    borrower = session.get(Borrower, borrower_id)
    
    if borrower is None:
        raise ValueError(f"\nCannot proceed. Borrower ID {borrower_id} does not exist.")

    return borrower


def check_if_email_exists(session, email: str):  # Separated from validate_borrower_email() so as to prevent multiple sessions from being opened in the related functions below
    """Check whether the email address provided already belongs to another Borrower in the database as email addresses must be unique. If cleared, returns the email address."""    
    
    test_borrower = session.query(Borrower).filter_by(email_address=email).first() 

    if test_borrower is not None:
        raise ValueError(f"\nCannot proceed. Email address {email} already exists for another borrower (ID: {test_borrower.id}) in the database.")
    
    return email


def normalize_borrower_phone(phone: str): 
    """Normalizes a Borrower phone number; occurs in add_borrower(), before adding the Borrower to the database. Returns the cleaned, normalized phone number."""

    phone = phone.strip()

    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.fullmatch(phone_pattern, phone)
    
    if not match:
        raise ValueError(f"\nCannot proceed. The phone number provided is not a valid phone number.") 
       
   
    clean_num = re.sub(r'\D', '', phone)  # If a valid phone number, Step 1: normalize format by removing any non-digits
    new_num = f"{clean_num[:3]}-{clean_num[3:6]}-{clean_num[6:10]}"  # Step 2: reformat phone number for readability and consistency in the database


    phone = new_num
    return phone


# Primary functions


def list_all_borrowers():
    """Get all Borrowers currently in the database, ordered by name. Returns a list of tuples containing the Borrower ID, name, email address, phone ('N/A' if None), and membership date; returns an empty list if no Borrowers exist."""
    
    with Session(engine) as session:

        borrowers = session.query(Borrower).order_by(Borrower.name).all()

        if not borrowers:            
            return []

        results = []

        for borrower in borrowers:
            phone = borrower.phone if borrower.phone is not None else "N/A"
            results.append(
                (borrower.id, borrower.name, borrower.email_address, phone, borrower.membership_date)    
            )  
       
        return results  


def update_borrower_email(borrower_id: int, new_email: str):
    """Update a Borrower's email address. Returns None if successful."""

    # Data Validation - Borrower ID
    borrower_id = validate_borrower_id(borrower_id)

    # Data Validation - New Email Address
    new_email = validate_borrower_email(new_email)    
   

    with Session(engine) as session:   
        
        # Check whether the Borrower ID exists in the database
        borrower = check_if_borrower_id_exists(session, borrower_id)

        # Check whether the new email address is already in the database 
        if new_email == borrower.email_address:
            raise ValueError("\nCannot update borrower email. The new email address provided is the same as the current email address on file.") 

        new_email = check_if_email_exists(session, new_email)
                   

        # If no errors above persist, update the Borrower email address
        borrower.email_address = new_email        
        
        try:            
            session.commit()            
                    
        except Exception:
            session.rollback()
            print("\nError updating borrower email in the database. Borrower email address not updated. Please try again. ")
            raise

        print(f"\nUpdated email address for {borrower.name} (Borrower ID: {borrower.id}) to {borrower.email_address}.")


def get_checkouts_by_borrower(borrower_id: int):
    """Get a list of Checkout activity for the designated Borrower. Returns a list of tuples (sorted by due date) containing the Checkout ID, Book title, Checkout date, due date, return date, and whether returned Books were returned late; returns an empty list if the Borrower does not have any Checkout activity."""
  
    # Data Validation - Borrower ID
    borrower_id = validate_borrower_id(borrower_id)

    with Session(engine) as session:

        # Check whether the Borrower ID exists in the database
        borrower = check_if_borrower_id_exists(session, borrower_id) 

        if not borrower.checkouts:            
            return []

        
        results = []
        
        for checkout in borrower.checkouts: 
            return_date = checkout.return_date if checkout.return_date is not None else "N/A"

            if checkout.return_date is not None:
                if checkout.due_date < checkout.return_date:
                    status = "Returned Late"

                else:
                    status = "Returned On-Time"

            elif checkout.due_date < date.today():
                status = "Overdue"

            else:
                status = "Checked Out"
                    
            results.append((checkout.id, checkout.book.title, checkout.checkout_date, checkout.due_date, return_date, status))

        sorted_results = sorted(results, key=lambda c: c[3])  # Sort by due date
        
        return sorted_results
    

def get_overdue_books():
    """Get a list of overdue Books. Returns a list of tuples (ordered by due date) containing the Checkout ID, Book title, Borrower ID, due date, and the number of days late; returns an empty list if no Books are overdue."""

    with Session(engine) as session:

        today = date.today()
        
        overdue_checkouts = session.query(Checkout).filter(Checkout.due_date < today, Checkout.return_date.is_(None)).order_by(Checkout.due_date).all()

        if not overdue_checkouts:            
            return []
        
        results = []

        for checkout in overdue_checkouts:            
            days_late = today - checkout.due_date
            results.append((checkout.id, checkout.book.title, checkout.borrower.id, checkout.due_date, days_late.days))

        return results


def add_borrower(name: str, email: str, membership_date: date, phone: str = None):
    """Add a new Borrower. Returns None if successful."""
        
    # Data Validation - Name
    if name is None:
        raise ValueError("\nCannot add borrower. Name is required.")

    if type(name) != str:
        raise TypeError("\nCannot add borrower. Name must be a string.")

    if name.strip() == "":
        raise ValueError("\nCannot add borrower. Name cannot be empty.")   

    name = name.strip().title()


    # Data Validation - Email    
    email = validate_borrower_email(email)       


    # Data Validation - Phone 
    if phone is not None:
        if type(phone) != str:
            raise TypeError("\nCannot add borrower. Phone Number must be a string.")
    
        if phone.strip() == "":
            raise ValueError("\nCannot add borrower. Phone Number can be None but cannot be an empty string.")
        
        phone = normalize_borrower_phone(phone)


    # Data Validation - Membership Date
    if membership_date is None:
        raise ValueError("\nCannot add borrower. Membership Date is required.")
    
    if type(membership_date) != date:
        raise TypeError("\nCannot add borrower. Membership Date must be a date.")

    if membership_date < date(2026, 1, 1):  # Prevents nonsensical membership years such as 1925, 1500, etc.
        raise ValueError("\nCannot add borrower. Membership Date cannot be earlier than 2026.")


    with Session(engine) as session:    

        # Check whether email address already exists in the database
        email = check_if_email_exists(session, email)  

        
        # If no errors above persist, create Borrower and add to the database
        new_borrower = Borrower(name=name, email_address=email, phone=phone, membership_date=membership_date)

        try:
            session.add(new_borrower)
            session.commit()            
        
        except Exception:
            session.rollback()
            print("\nError adding borrower to the database. Borrower not added. Please try again. ")
            raise

        print(f"\nAdded: {new_borrower}")


def delete_borrower(borrower_id: int):
    """Delete a Borrower if they do not currently have any active Checkouts. If there are no active checkouts, any associated Checkout history is deleted before deleting the Borrower so as to prevent errors. Returns True if successful; returns False if there is an active checkout preventing the deletion."""

    # Data Validation - Borrower ID
    borrower_id = validate_borrower_id(borrower_id)   
    

    with Session(engine) as session:
    
        # Check whether the Borrower ID exists in the database
        borrower = check_if_borrower_id_exists(session, borrower_id)

        
        for checkout in borrower.checkouts:

            # Check whether there are any active Checkouts
            if checkout.return_date is None:
                print(f"\nCannot delete borrower as they currently have a book checked out.")
                return False

            # Delete Checkout history
            session.delete(checkout)
            

        # If no errors above persist, delete the Borrower from the database
        try:            
            session.delete(borrower)
            session.commit()            
        
        except Exception:
            session.rollback()
            print("\nError deleting borrower from the database. Borrower not deleted. Please try again. ")
            raise
        
        print(f"\nDeleted borrower with ID {borrower_id} from the database.")
        return True       