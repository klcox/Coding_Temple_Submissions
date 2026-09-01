from datetime import date

from helper_menu_functions import (
    retry_or_return, collect_author_id, collect_book_id, collect_borrower_id
)

from records_books import (
    add_author, add_book, list_all_authors, list_all_books, delete_book   
)

from records_borrowers import (
    add_borrower, list_all_borrowers, update_borrower_email, get_checkouts_by_borrower, get_overdue_books, delete_borrower
)

from search_checkout_return import (
    list_available_books, find_books_by_author, find_books_by_keyword, find_books_by_era, checkout_book, return_book   
)


# Menu calls to associated functions:


# --------------
# BOOK RECORDS
# --------------


def menu_list_all_authors(): 
    """Displays all Authors currently in the database."""

    print("\nFetching authors...\n")

    authors = list_all_authors()

    if not authors:
        print("\nCurrently, there are no authors in the database.")
        print("\nReturning to the main menu...")
        return  # To main CLI menu

    print(f"{'ID':<5} | {'Author Name':<25}")
    print("-" * 70)
    for item in authors:
        print(f"{item[0]:<5} | {item[1]:<25}") 

    print("\nReturning to the main menu...")
    return  # To main CLI menu


def menu_list_all_books():
    """Displays all Books currently in the database."""

    print("\nFetching books...\n")

    books = list_all_books()

    if not books:
        print("\nCurrently, there are no books in the database.")
        print("\nReturning to the main menu...")
        return  # To main CLI menu

    print(f"{'ID':<5} | {'Title':<40} | {'Author(s)':<40}")
    print("-" * 100)
    for item in books:
        print(f"{item[0]:<5} | {item[1]:<40} | {item[2]:<40}")   

    print("\nReturning to the main menu...")
    return  # To main CLI menu    


def menu_add_author():
    """Prompts for Author details and adds to the database."""

    while True:

        print("\nFor the author you would like to add:")

        name = input("\nWhat is the author's name? ")
        bio = input("\nPlease enter a bio for the author or press Enter to skip: ")

        if bio.strip() == "":
            bio = None


        print("\nAttempting to add author to the database...")

        try:
            add_author(name, bio)            

        except Exception as error_message:  # Exception includes all error types from the add_author() function
            print(error_message) 

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu        
        
        print("\nReturning to the main menu...")
        return  # To main CLI menu
    
    
def menu_add_book():
    """Prompts for Book details and adds to the database."""

    while True:

        print("\nFor the book you would like to add:")

        # Title, ISBN
        title = input("\nWhat is the book title? ")
        isbn = input("\nWhat is the ISBN? (Numbers only, 13 digits) ")


        # Year Published
        try:
            year_published = int(input("\nWhat year was the book originally published? (Use a negative number for BCE) ").strip())

        except ValueError:
            print("\nCannot attempt to add book. Year published must be an integer.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu


        # Author ID(s)
        author_ids = []

        try:
            num_authors = int(input("\nHow many authors are associated with the book? (Enter 1 or 2) ").strip())

        except ValueError:
            print("\nCannot attempt to add book. Number of authors must be an integer.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")    
                return  # To main CLI menu

        if num_authors == 1:
            author_id_A = collect_author_id()

            if author_id_A is None:
                print("\nReturning to the main menu...")
                return  # To main CLI menu

            author_ids.append(author_id_A)            

        elif num_authors == 2:

            print("\nFor the first author:")
            author_id_B = collect_author_id()

            print("\nFor the second author:")
            author_id_C = collect_author_id()

            if author_id_B is None or author_id_C is None:
                print("\nReturning to the main menu...")
                return  # To main CLI menu
            
            author_ids.extend([author_id_B, author_id_C])

        else:  # Catches the case where the user does not respond with 1 or 2 to the number of authors
            print("\nCannot proceed. Response for the previous question must be 1 or 2.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")                                
                return  # To main CLI menu   
            

        # Available Copies
        available_copies = input("\nHow many copies are available? (If 1, press Enter to skip) ").strip()

        if available_copies == "":
            available_copies = 1

        else:
            try:
                available_copies = int(available_copies)

            except ValueError:
                print("\nCannot attempt to add book. For available copies, press Enter or enter an integer.")

                if retry_or_return():
                    continue  # Re-run the function
    
                else:
                    print("\nReturning to the main menu...")                                
                    return  # To main CLI menu             


        print("\nAttempting to add book to the database...")

        try:
            add_book(title, isbn, year_published, author_ids, available_copies)           

        except Exception as error_message:
            print(error_message) 

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu       
        
        print("\nReturning to the main menu...")     
        return  # To main CLI menu 

def menu_delete_book():
    """Prompts for the Book ID and deletes from the database (if there are no active checkouts)."""

    while True:

        print("\nFor the book you would like to delete:")

        book_id = collect_book_id()

        if book_id is None:
            print("\nReturning to the main menu...")
            return  # To main CLI menu

        print("\nAttempting to delete book from the database...\n")
        print("**Note: The list displays books with copies available for checkout. In order to delete a book, it cannot have any active checkouts.\nSince some books may have several copies, active checkouts will be reviewed before proceeding with deletion.**")
        
        try:
            deleted = delete_book(book_id)            

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu

        if deleted:
            print("\nReturning to the main menu...")      
            return  # To main CLI menu 

        else:  # Covers the case where the Book cannot be deleted due to an active Checkout
            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu


# -----------------
# BORROWER RECORDS
# -----------------


def menu_list_all_borrowers():
    """Displays all Borrowers currently in the database."""

    print("\nFetching borrowers...\n")

    borrowers = list_all_borrowers()

    if not borrowers:
        print("\nCurrently, there are no borrowers in the database.")
        print("\nReturning to the main menu...")
        return  # To main CLI menu

    print(f"{'ID':<5} | {'Name':<25} | {'Email':<30}")
    print("-" * 80)
    for item in borrowers:
        print(f"{item[0]:<5} | {item[1]:<25} | {item[2]:<30}")   

    print("\nReturning to the main menu...")
    return  # To main CLI menu   
     

def menu_update_borrower_email():
    """Prompts for Borrower ID and updates the email address in the database."""

    while True:

        print("\nFor the borrower profile you would like to update:")

        borrower_id = collect_borrower_id()

        if borrower_id is None:
            print("\nReturning to the main menu...")
            return  # To main CLI menu
        
        new_email = input("\nWhat is the borrower's new email address? ")


        print("\nAttempting to update borrower profile...")

        try:
            update_borrower_email(borrower_id, new_email)            

        except Exception as error_message:
            print(error_message) 

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu        
                    
        print("\nReturning to the main menu...")
        return  # To main CLI menu


def menu_get_checkouts_by_borrower():
    """Prompts for Borrower ID and displays their Checkout history."""

    while True:
        print("\nFor the borrower activity you would like to check:")

        borrower_id = collect_borrower_id()  

        if borrower_id is None:
            print("\nReturning to the main menu...")
            return  # To main CLI menu

        print("\nFetching borrower checkout activity...")

        try:
            checkout_history = get_checkouts_by_borrower(borrower_id) 

        except Exception as error_message:
            print(error_message) 

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu      

        if not checkout_history:
            print(f"\nBorrower with ID {borrower_id} does not have any checkout activity.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu

        print(f"\nCheckout history for borrower with ID {borrower_id}:\n")        
        print(f"{'Checkout ID':<14} | {'Book Title':<40} | {'Checkout Date':<15} | {'Due Date':<15} | {'Return Date':<15} | {'Status':<12}")
        print("-" * 130)
        for item in checkout_history:
            print(f"{item[0]:<14} | {item[1]:<40} | {str(item[2]):<15} | {str(item[3]):<15} | {str(item[4]):<15} | {item[5]:<12}")

        print("\nReturning to the main menu...")
        return  # To main CLI menu  


def menu_get_overdue_books():
    """Displays all overdue Checkouts."""

    print("\nFetching overdue checkouts...")

    overdue_checkouts = get_overdue_books() 

    if not overdue_checkouts:
        print("\nNo books currently overdue.")
        print("\nReturning to the main menu...")
        return  # To main CLI menu       

    print("\nOverdue checkouts:\n")
    print(f"{'Checkout ID':<5} | {'Book Title':<40} | {'Borrower ID':<14} | {'Due Date':<15} | {'Days Late':<5}")
    print("-" * 90)
    for item in overdue_checkouts:
        print(f"{item[0]:<5} | {item[1]:<40} | {item[2]:<14} | {str(item[3]):<15} | {item[4]:<5}")

    print("\nReturning to the main menu...")
    return  # To main CLI menu 


def menu_add_borrower():
    """Prompts for the Borrower details and adds to the database."""
   
    while True:

        print("\nFor the borrower you would like to add:")

        name = input("\nWhat is the borrower's name? ")
        email = input("\nWhat is the borrower's email address? ")
        phone = input("\nWhat is the borrower's phone number? (Press Enter to skip) ")

        if phone.strip() == "":
            phone = None


        print("\nAttempting to add borrower to the database...")

        try:
            add_borrower(name, email, phone)            

        except Exception as error_message:
            print(error_message) 

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu        
        
        print("\nReturning to the main menu...")            
        return  # To main CLI menu


def menu_delete_borrower():
    """Prompts for Borrower ID and deletes them from the database (if they do not have any active checkouts)."""
    
    while True:

        print("\nFor the borrower you would like to delete:")

        borrower_id = collect_borrower_id() 

        if borrower_id is None:
            print("\nReturning to the main menu...")
            return  # To main CLI menu 

        print("\nAttempting to delete borrower from the database...\n")
        print("**Note: In order to delete a borrower, they cannot have any active checkouts.\nActive checkouts will be reviewed before proceeding with deletion.**")

        try:
            deleted = delete_borrower(borrower_id)           

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu

        if deleted:
            print("\nReturning to the main menu...")
            return  # To main CLI menu             

        else:  # Covers the case where the Borrower cannot be deleted due to an active Checkout
            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu


# ----------------------------
# SEARCH, CHECKOUT, & RETURN
# ----------------------------


def menu_list_available_books():
    """Displays all Books with copies available."""

    print("\nFetching available books...")

    books = list_available_books()    
    
    if not books:
        print("\nNo books currently available.")
        print("\nReturning to the main menu...")
        return  # To main CLI menu

    print("\nBooks available for checkout:\n")
    print(f"{'ID':<5} | {'Title':<40} | {'Author(s)':<40}")
    print("-" * 100)
    for item in books:
        print(f"{item[0]:<5} | {item[1]:<40} | {item[2]:<40}")

    print("\nReturning to the main menu...")
    return  # To main CLI menu


def menu_find_books_by_author():
    """Prompts for Author name and displays all Books whose Author contains the name provided."""
   
    while True:

        author_name = input("\nPlease enter the author name you would like to search: ")

        print("\nSearching for books with matching author name...")

        try:
            results = find_books_by_author(author_name)       
                    
        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu

        if not results:
            print(f"\nNo books found with author name(s) containing '{author_name}'.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu 

        print(f"\nBooks by authors whose name contains '{author_name}':\n")    
        print(f"{'ID':<5} | {'Author(s)':<40} | {'Title':<40}")
        print("-" * 100)        
        for item in results:
            print(f"{item[0]:<5} | {item[1]:<40} | {item[2]:<40}")

        print("\nReturning to the main menu...")
        return  # To main CLI menu


def menu_find_books_by_keyword():
    """Prompts for keyword and displays all Books whose title contains the keyword provided."""
   
    while True:

        keyword = input("\nPlease enter the keyword you would like to search: ")

        print("\nSearching for books with matching keyword...")

        try:
            results = find_books_by_keyword(keyword)

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu

        if not results:
            print(f"\nNo book titles found containing '{keyword}'.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu 

        print(f"\nBooks whose title contains '{keyword}':\n")    
        print(f"{'ID':<5} | {'Title':<40} | {'Author(s)':<40}")
        print("-" * 100)
        for item in results:
            print(f"{item[0]:<5} | {item[1]:<40} | {item[2]:<40}")

        print("\nReturning to the main menu...")
        return  # To main CLI menu


def menu_find_books_by_era():
    """Prompts for era and displays all Books whose year of publication matches the era provided."""
   
    while True:
        era = input("\nPlease enter the era you would like to search (CE or BCE): ")

        print("\nSearching for books from the selected era...")

        try:
            results = find_books_by_era(era)

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu        
        
        if not results:
            print(f"\nNo books found from this era: {era}.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")
                return  # To main CLI menu 

        print(f"\nBooks from the era '{era}':\n")    
        print(f"{'ID':<5} | {'Title':<40} | {'Author(s)':<40}")
        print("-" * 100)        
        for item in results:
            print(f"{item[0]:<5} | {item[1]:<40} | {item[2]:<40}")

        print("\nReturning to the main menu...")
        return  # To main CLI menu


def menu_checkout_book():
    """Prompts for Book ID, Borrower ID, and Checkout date, then checks out the Book."""

    while True:

        print("\nFor the book you would like to checkout:")

        book_id = collect_book_id()  

        if book_id is None:
            print("\nReturning to the main menu...")
            return  # To main CLI menu       

        borrower_id = collect_borrower_id()

        if borrower_id is None:
            print("\nReturning to the main menu...")
            return  # To main CLI menu 


        # Determine if Checkout Date is Today
        checkout_is_today = input("\nIs the checkout date today? (Y/N) ").strip().upper()

        if checkout_is_today == "Y":  # If YES, None will become "today" in checkout_book()            
            checkout_date = None  

        elif checkout_is_today == "N":  # If NO, prompt for the date
            print("\n**Note: The checkout date cannot be earlier than 2 days ago nor a future date.**")
            selected_date = input("Please enter the checkout date (YYYY-MM-DD): ").strip()               
            
            try:
                checkout_date = date.fromisoformat(selected_date)                

            except ValueError:
                print("\nCannot attempt to checkout book. Checkout date must match the format YYYY-MM-DD.")

                if retry_or_return():
                    continue  # Re-run the function
    
                else:
                    print("\nReturning to the main menu...")                                
                    return  # To main CLI menu              

        else:  # Catches the case where the user does not respond Y/N to verifying the Checkout date
            print("\nCannot attempt to checkout book. Response for the previous question must be Y or N.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")                                
                return  # To main CLI menu


        # Attempt checkout
        print("\nAttempting to checkout book...")

        try:
            checkout_book(book_id, borrower_id, checkout_date)            

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")                                
                return  # To main CLI menu        

        print("\nReturning to the main menu...")                                
        return  # To main CLI menu


def menu_return_book():
    """Prompts for the Checkout ID and returns the Book."""

    while True:

        print("\nFor the book you would like to return:")

        # Check if the user knows the Checkout ID
        know_checkout_id = input("\nDo you know the Checkout ID number? (Y/N) ").strip().upper()

        if know_checkout_id == "Y":  # If YES, collect the Checkout ID
        
            try:
                checkout_id = int(input("\nWhat is the checkout ID number? ").strip())

            except ValueError:
                print("\nCannot attempt to return book. Checkout ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function
                

        elif know_checkout_id == "N":  # If NO, gather Checkout information by Borrower and prompt user for Checkout ID

            borrower_id = collect_borrower_id()  

            if borrower_id is None:
                print("\nReturning to the main menu...")
                return  # To main CLI menu 


            print("\nGathering borrowing activity...\n")        

            try:
                checkouts = get_checkouts_by_borrower(borrower_id)  # Use Borrower ID to gather Checkout activity                        

            except Exception as error_message:
                print(error_message)

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            if not checkouts:  # If borrower does not have any checkout activity
                print("\nCannot attempt to return book as the borrower does not have any checkout activity.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            print(f"\nCheckout history for borrower with ID {borrower_id}:\n")
            print(f"{'Checkout ID':<14} | {'Book Title':<40} | {'Checkout Date':<15} | {'Due Date':<15} | {'Return Date':<15} | {'Status':<12}")  # Present the checkouts to the user for selection              
            print("-" * 130)
            for item in checkouts:
                print(f"{item[0]:<14} | {item[1]:<40} | {str(item[2]):<15} | {str(item[3]):<15} | {str(item[4]):<15} | {item[5]:<12}")           

        
            try:
                selected_checkout_id = int(input("\nPlease enter the selected checkout ID for the book you are returning: ").strip())                

            except ValueError:
                print("\nThat is not a valid selection. Checkout ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function


            # Check that the ID entered by the user matches one of the IDs from the list above
            if not any(checkout[0] == selected_checkout_id for checkout in checkouts):
                print(f"\nThat is not a valid selection. Checkout ID {selected_checkout_id} is not one of the matching checkouts. Please select from the list provided.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function       
            
            checkout_id = selected_checkout_id

                
        else:  # Catches the case where the user does not respond Y/N to knowing the Checkout ID
            print("\nCannot attempt to return book. Response for the previous question must be Y or N.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                return  # To menu function  
            

        # Attempt return
        print("\nAttempting to return book...")
        
        try:
            book_returned = return_book(checkout_id)           

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")                                
                return  # To main CLI menu

        if book_returned:           
           print("\nReturning to the main menu...")                                
           return  # To main CLI menu

        else:  # Covers the case where the Book cannot be returned since it was already returned
            if retry_or_return():
                continue  # Re-run the function

            else:
                print("\nReturning to the main menu...")                                
                return  # To main CLI menu