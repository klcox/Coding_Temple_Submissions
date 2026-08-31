from datetime import date

from helper_menu_functions import(
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

    print("Fetching authors...")

    authors = list_all_authors()

    if not authors:
        print("Returning to the main menu...")
        return  # To main CLI menu

    print(f"{'ID':<5}|{'Author Name':<55}")
    print("-" * 70)
    for item in authors:
        print(f"{item[0]:<5} {item[1]:<55}") 

    print("Returning to the main menu...")
    return  # To main CLI menu


def menu_list_all_books():
    """Displays all Books currently in the database."""

    print("Fetching books...")

    books = list_all_books()

    if not books:
        print("Returning to the main menu...")
        return  # To main CLI menu

    print(f"{'ID':<5}|{'Title':<55}|{'Author(s)':<50}")
    print("-" * 100)
    for item in books:
        print(f"{item[0]:<5} {item[1]:<55} {item[2]:<50}")   

    print("Returning to the main menu...")
    return  # To main CLI menu    


def menu_add_author():
    """Prompts for Author details and adds to the database."""

    while True:

        print("For the author you would like to add:")

        name = input("What is the author's name? ")
        bio = input("Please enter a bio for the author or press Enter to skip: ")

        if bio.strip() == "":
            bio = None


        print("Attempting to add author to the database...")

        try:
            author = add_author(name, bio)            

        except Exception as error_message:  # Exception includes all error types from the add_author() function
            print(error_message) 

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu

        print(f"Added: {author}")
        
        print("Returning to the main menu...")
        return  # To main CLI menu
    
    
def menu_add_book():
    """Prompts for Book details and adds to the database."""

    while True:

        print("For the book you would like to add:")

        # Title, ISBN
        title = input("What is the book title? ")
        isbn = input("What is the ISBN? (Numbers only, 13 digits) ")


        # Year Published
        try:
            year_published = int(input("What year was the book originally published? (Use a negative number for BCE) "))

        except ValueError:
            print("Cannot attempt to add book. Year published must be an integer.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu


        # Author ID(s)
        author_ids = []

        try:
            num_authors = int(input("How many authors are associated with the book? (Enter 1 or 2) ").strip())

        except ValueError:
            print("Cannot attempt to add book. Number of authors must be an integer.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")    
                return  # To main CLI menu

        if num_authors == 1:
            author_id_A = collect_author_id()

            if author_id_A is None:
                print("Returning to the main menu...")
                return  # To main CLI menu

            author_ids.append(author_id_A)            

        elif num_authors == 2:

            print("For the first author:")
            author_id_B = collect_author_id()

            print("For the second author:")
            author_id_C = collect_author_id()

            if author_id_B is None or author_id_C is None:
                print("Returning to the main menu...")
                return  # To main CLI menu
            
            author_ids.extend([author_id_B, author_id_C])

        else:  # Catches the case where the user does not respond with 1 or 2 to the number of authors
            print("Cannot proceed. Response for the previous question must be 1 or 2.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")                                
                return  # To main CLI menu   
            

        # Available Copies
        available_copies = input("How many copies are available? (If 1, press Enter to skip) ").strip()

        if available_copies == "":
            available_copies = 1

        else:
            try:
                available_copies = int(available_copies)

            except ValueError:
                print("Cannot attempt to add book. For available copies, press Enter or enter an integer.")

                if retry_or_return():
                    continue  # Re-run the function
    
                else:
                    print("Returning to the main menu...")                                
                    return  # To main CLI menu             


        print("Attempting to add book to the database...")

        try:
            book = add_book(title, isbn, year_published, author_ids, available_copies)           

        except Exception as error_message:
            print(error_message) 

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu

        print(f"Added: {book}")
        
        print("Returning to the main menu...")     
        return  # To main CLI menu 

def menu_delete_book():
    """Prompts for the Book ID and deletes from the database (if there are no active checkouts)."""

    while True:

        print("For the book you would like to delete:")

        book_id = collect_book_id()

        if book_id is None:
            print("Returning to the main menu...")
            return  # To main CLI menu

        print("Attempting to delete book from the database...")
        print("**Note: The list displays books with copies available for checkout. In order to delete a book, it cannot have any active checkouts. Since some books may have several copies, active checkouts will be reviewed before proceeding with deletion.**")
        
        try:
            deleted = delete_book(book_id)            

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu

        if deleted:
            print("Returning to the main menu...")      
            return  # To main CLI menu 

        else:
            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu


# -----------------
# BORROWER RECORDS
# -----------------


def menu_list_all_borrowers():
    """Displays all Borrowers currently in the database."""

    print("Fetching borrowers...")

    borrowers = list_all_borrowers()

    if not borrowers:
        print("Returning to the main menu...")
        return  # To main CLI menu

    print(f"{'Borrower ID':<5}|{'Name':<25}|{'Email':<40}")
    print("-" * 80)
    for item in borrowers:
        print(f"{item[0]:<5} {item[1]:<25} {item[2]:<40}")   

    print("Returning to the main menu...")
    return  # To main CLI menu   
     

def menu_update_borrower_email():
    """Prompts for Borrower ID and updates the email address in the database."""

    while True:

        print("For the borrower profile you would like to update:")

        borrower_id = collect_borrower_id()

        if borrower_id is None:
            print("Returning to the main menu...")
            return  # To main CLI menu
        
        new_email = input("What is the borrower's new email address? ")


        print("Attempting to update borrower profile...")

        try:
            updated_borrower_profile = update_borrower_email(borrower_id, new_email)            

        except Exception as error_message:
            print(error_message) 

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu

        print(f"Updated email address for {updated_borrower_profile.name} (Borrower ID: {borrower_id}) to {updated_borrower_profile.email_address}.")
                    
        print("Returning to the main menu...")
        return  # To main CLI menu


def menu_get_checkouts_by_borrower():
    """Prompts for Borrower ID and displays their Checkout history."""

    while True:
        print("For the borrower activity you would like to check:")

        borrower_id = collect_borrower_id()  

        if borrower_id is None:
            print("Returning to the main menu...")
            return  # To main CLI menu

        print("Fetching borrower checkout activity...")

        try:
            checkout_history = get_checkouts_by_borrower(borrower_id) 

        except Exception as error_message:
            print(error_message) 

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu      

        if not checkout_history:
            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu

        print(f"Checkout history for borrower with ID {borrower_id}:")
        
        print(f"{'Checkout ID':<5}|{'Book Title':<55}|{'Checkout Date':<15}|{'Due Date':<15}|{'Return Date':<15}|{'Late Status':<10}")
        print("-" * 100)
        for item in checkout_history:
            print(f"{item[0]:<5} {item[1]:<55} {item[2]:<15} {item[3]:<15} {item[4]:<15} {item[5]:<10}")

        print("Returning to the main menu...")
        return  # To main CLI menu  


def menu_get_overdue_books():
    """Displays all overdue Checkouts."""

    print("Fetching overdue checkouts...")

    overdue_checkouts = get_overdue_books() 

    if not overdue_checkouts:
        print("Returning to the main menu...")
        return  # To main CLI menu       

    print("Overdue checkouts:")

    print(f"{'Checkout ID':<5}|{'Book Title':<55}|{'Borrower ID':<5}|{'Due Date':<15}|{'Days Late':<5}")
    print("-" * 90)
    for item in overdue_checkouts:
        print(f"{item[0]:<5} {item[1]:<55} {item[2]:<5} {item[3]:<15} {item[4]:<5}")

    print("Returning to the main menu...")
    return  # To main CLI menu 


def menu_add_borrower():
    """Prompts for the Borrower details and adds to the database."""
   
    while True:

        print("For the borrower you would like to add:")

        name = input("What is the borrower's name? ")
        email = input("What is the borrower's email address? ")
        phone = input("What is the borrower's phone number? (Press Enter to skip) ")

        if phone.strip() == "":
            phone = None


        print("Attempting to add borrower to the database...")

        try:
            borrower = add_borrower(name, email, phone)            

        except Exception as error_message:
            print(error_message) 

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu

        print(f"Added: {borrower}")
        
        print("Returning to the main menu...")            
        return  # To main CLI menu


def menu_delete_borrower():
    """Prompts for Borrower name and deletes them from the database (if they do not have any active checkouts)."""
    
    while True:

        print("For the borrower you would like to delete:")

        borrower_id = collect_borrower_id() 

        if borrower_id is None:
            print("Returning to the main menu...")
            return  # To main CLI menu 

        print("Attempting to delete borrower from the database...")
        print("**Note: In order to delete a borrower, they cannot have any active checkouts. Active checkouts will be reviewed before proceeding with deletion.**")

        try:
            deleted = delete_borrower(borrower_id)           

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu

        if deleted:
            print("Returning to the main menu...")
            return  # To main CLI menu             

        else:
            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu


# ----------------------------
# SEARCH, CHECKOUT, & RETURN
# ----------------------------


def menu_list_available_books():
    """Displays all Books with copies available."""

    print("Fetching available books...")

    books = list_available_books()    
    
    if not books:
        print("Returning to the main menu...")
        return  # To main CLI menu

    print("Books available for checkout:")
    print(f"{'ID':<5}|{'Title':<55}|{'Author(s)':<50}")
    print("-" * 100)
    for item in books:
        print(f"{item[0]:<5} {item[1]:<55} {item[2]:<50}")

    print("Returning to the main menu...")
    return  # To main CLI menu


def menu_find_books_by_author():
    """Prompts for Author name and displays all Books whose Author contains the name provided."""
   
    while True:

        name = input("Please enter the author name you would like to search: ")

        print("Searching for books with matching author name...")

        try:
            results = find_books_by_author(name)       
                    
        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu

        if not results:
            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu 

        print(f"Books by authors whose name contains '{name}':")    
        print(f"{'ID':<5}|{'Author(s)':<50}|{'Title':<55}")
        print("-" * 100)        
        for item in results:
            print(f"{item[0]:<5} {item[1]:<50} {item[2]:<55}")

        print("Returning to the main menu...")
        return  # To main CLI menu


def menu_find_books_by_keyword():
    """Prompts for keyword and displays all Books whose title contains the keyword provided."""
   
    while True:

        keyword = input("Please enter the keyword you would like to search: ")

        print("Searching for books with matching keyword...")

        try:
            results = find_books_by_keyword(keyword)

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu

        if not results:
            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu 

        print(f"Books whose title contains '{keyword}':")    
        print(f"{'ID':<5}|{'Title':<55}|{'Author(s)':<50}")
        print("-" * 100)
        for item in results:
            print(f"{item[0]:<5} {item[1]:<55} {item[2]:<50}")

        print("Returning to the main menu...")
        return  # To main CLI menu


def menu_find_books_by_era():
    """Prompts for era and displays all Books whose year of publication matches the era provided."""
   
    while True:
        era = input("Please enter the era you would like to search (CE or BCE): ")

        print("Searching for books from the selected era...")

        try:
            results = find_books_by_era(era)

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu        
        
        if not results:
            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")
                return  # To main CLI menu 

        print(f"Books from the era '{era}':")    
        print(f"{'ID':<5}|{'Title':<55}|{'Author(s)':<50}")
        print("-" * 100)        
        for item in results:
            print(f"{item[0]:<5} {item[1]:<55} {item[2]:<50}")

        print("Returning to the main menu...")
        return  # To main CLI menu


def menu_checkout_book():
    """Prompts for Book ID, Borrower ID, and Checkout date, then checks out the book."""

    while True:

        print("For the book you would like to checkout:")

        book_id = collect_book_id()  

        if book_id is None:
            print("Returning to the main menu...")
            return  # To main CLI menu       

        borrower_id = collect_borrower_id()

        if borrower_id is None:
            print("Returning to the main menu...")
            return  # To main CLI menu 


        # Determine if Checkout Date is Today
        checkout_is_today = input("Is the checkout date today? (Y/N) ").strip().upper()

        if checkout_is_today == "Y":  # If YES, None will become "today" in checkout_book()
            print("Thank you for confirming the checkout date is today.")
            checkout_date = None  

        elif checkout_is_today == "N":  # If NO, prompt for the date
            print("**Note: The checkout date cannot be earlier than 2 days ago nor a future date.**")
            selected_date = input("Please enter the checkout date (YYYY-MM-DD): ").strip()

            print("Verifying checkout date...")       
            
            try:
                checkout_date = date.fromisoformat(selected_date)
                print("Checkout date confirmed.")

            except ValueError:
                print("Cannot attempt to checkout book. Checkout date must match the format YYYY-MM-DD.")

                if retry_or_return():
                    continue  # Re-run the function
    
                else:
                    print("Returning to the main menu...")                                
                    return  # To main CLI menu  

        else:  # Catches the case where the user does not respond Y/N to verifying the Checkout date
            print("Cannot attempt to checkout book. Response for the previous question must be Y or N.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")                                
                return  # To main CLI menu


        # Attempt checkout
        print("Attempting to checkout book...")

        try:
            checkout = checkout_book(book_id, borrower_id, checkout_date)            

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")                                
                return  # To main CLI menu

        print(f"Checkout confirmed. Checkout ID: {checkout.id}, Due Date: {checkout.due_date}")

        print("Returning to the main menu...")                                
        return  # To main CLI menu


def menu_return_book():
    """Prompts for the checkout ID and returns the book."""

    while True:

        print("For the book you would like to return:")

        # Check if the user knows the Checkout ID
        know_checkout_id = input("Do you know the Checkout ID number? (Y/N) ").strip().upper()

        if know_checkout_id == "Y":  # If YES, collect the Checkout ID
        
            try:
                checkout_id = int(input("What is the checkout ID number? "))

            except ValueError:
                print("Cannot attempt to return book. Checkout ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function
                

        elif know_checkout_id == "N":  # If NO, gather Checkout information by Borrower and prompt user for Checkout ID

            borrower_id = collect_borrower_id()  

            if borrower_id is None:
                print("Returning to the main menu...")
                return  # To main CLI menu 


            print("Gathering borrowing activity...")        

            try:
                checkouts = get_checkouts_by_borrower(borrower_id)  # Use Borrower ID to gather Checkout activity                        

            except Exception as error_message:
                print(error_message)

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            if not checkouts:  # If borrower does not have any checkout activity
                print("Cannot attempt to return book as the borrower does not have any checkout activity.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            print(f"Checkout history for borrower with ID {borrower_id}:")  # Present the checkouts to the user for selection                
            print(f"{'Checkout ID':<5}|{'Book Title':<55}|{'Checkout Date':<15}|{'Due Date':<15}")
            print("-" * 100)
            for item in checkouts:
                print(f"{item[0]:<5} {item[1]:<55} {item[2]:<15} {item[3]:<15}")

        
            try:
                selected_checkout_id = int(input("Please enter the selected checkout ID for the book you are returning: "))                

            except ValueError:
                print("That is not a valid selection. Checkout ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function


            # Check that the ID entered by the user matches one of the IDs from the list above
            if not any(checkout[0] == selected_checkout_id for checkout in checkouts):
                print(f"That is not a valid selection. Checkout ID {selected_checkout_id} is not one of the matching checkouts. Please select from the list provided.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function       
            
            checkout_id = selected_checkout_id

                
        else:  # Catches the case where the user does not respond Y/N to knowing the Checkout ID
            print("Cannot attempt to return book. Response for the previous question must be Y or N.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                return  # To menu function  
            

        # Attempt return
        print("Attempting to return book...")
        
        try:
            book_returned = return_book(checkout_id)           

        except Exception as error_message:
            print(error_message)

            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")                                
                return  # To main CLI menu

        if book_returned:           
           print("Returning to the main menu...")                                
           return  # To main CLI menu

        else:
            if retry_or_return():
                continue  # Re-run the function

            else:
                print("Returning to the main menu...")                                
                return  # To main CLI menu