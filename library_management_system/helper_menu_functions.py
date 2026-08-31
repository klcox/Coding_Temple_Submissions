from records_books import list_all_authors
from records_borrowers import list_all_borrowers
from search_checkout_return import (list_available_books)


def retry_or_return():
    """In the event of an error, prompts user to try again (re-run the function) or to return to the main CLI menu."""

    while True:

        retry = input("Press Y to try again or N to return to the main menu. ").strip().upper()

        if retry == "Y":
           return True  # Re-runs the associated function loop

        elif retry == "N":
            return False # Exits the associated function loop and ultimately returns to the main CLI menu

        else:
            print("Invalid entry. Response for the previous question must be Y or N.")  # Continues the loop until a valid response is received


def collect_author_id():
    """Determines how the user would like to provide the Author ID - either directly or by selecting from a list. Collects and returns the Author ID."""

    while True:

        # Check if the user knows the Author ID
        know_author_id = input("Do you know the Author ID number? (Y/N) ").strip().upper()

        if know_author_id == "Y":  # If YES, collect the Author ID
                      
            try:
                author_id = int(input("What is the author's ID number? ").strip())               

            except ValueError:
                print("Cannot proceed. Author ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            return author_id
        

        elif know_author_id == "N":  # If NO, have the user select from a list of authors
                    
            print("Fetching a list of authors and their associated IDs for your selection...")        

            authors = list_all_authors()  

            if not authors:  # If no authors are found
                print("Cannot proceed as there are no authors currently in the database.")
                return  # To the menu function  
                                

            print("Please locate the Author ID from the list of authors below: ")     
        
            print(f"{'ID':<5}|{'Author Name':<55}")
            print("-" * 70)
            for author in authors:
                print(f"{author[0]:<5} {author[1]:<55}")


            try:
                selected_author_id = int(input("Please enter the selected Author ID: "))                

            except ValueError:
                print("That is not a valid selection. Author ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function
                

            # Check that the ID entered by the user matches one of the IDs from the list above
            if not any(author[0] == selected_author_id for author in authors):
                print(f"That is not a valid selection. Author ID {selected_author_id} is not listed above. Please select from the list provided.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            return selected_author_id


        else:  # Catches the case where the user does not respond Y/N to knowing the Author ID
            print("Cannot proceed. Response for the previous question must be Y or N.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                return  # To menu function  
            

def collect_book_id():
    """Determine how the user would like to provide the Book ID - either directly or by selecting from a list of available books. Collects and returns the Book ID."""

    while True:

        # Check if the user knows the Book ID 
        know_book_id = input("Do you know the Book ID number? (Y/N) ").strip().upper()

        if know_book_id == "Y":  # If YES, collect the Book ID
            
            try:
                book_id = int(input("What is the book's ID number? "))

            except ValueError:
                print("Cannot proceed. Book ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function
    
                else:
                    return  # To menu function    

            return book_id
                 

        elif know_book_id == "N":  # If NO, have the user select from a list of available books

            print("Fetching a list of available books and their associated IDs for your selection...")   

            books = list_available_books()     

            if not books:  # If no books are found
                print("Cannot proceed as no books are currently available.")
                return  # To the menu function  
                                

            print("Please locate the Book ID from the list of books below: ")     
        
            print(f"{'ID':<5}|{'Title':<55}|{'Author(s)':<50}")
            print("-" * 100)
            for item in books:
                print(f"{item[0]:<5} {item[1]:<55} {item[2]:<50}")


            try:
                selected_book_id = int(input("Please enter the selected Book ID: "))                

            except ValueError:
                print("That is not a valid selection. Book ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function
                

            # Check that the ID entered by the user matches one of the IDs from the list above
            if not any(book[0] == selected_book_id for book in books):
                print(f"That is not a valid selection. Book ID {selected_book_id} is not listed above. Please select from the list provided.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            return selected_book_id


        else:  # Catches the case where the user does not respond Y/N to knowing the Book ID
            print("Cannot proceed. Response for the previous question must be Y or N.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                return  # To menu function      


def collect_borrower_id():
    """Determine how the user would like to provide the Borrower ID - either directly or by selecting from a list. Collects and returns the Borrower ID."""

    while True:

        # Check if the user knows the Borrower ID 
        know_borrower_id = input("Do you know the Borrower ID number? (Y/N) ").strip().upper()

        if know_borrower_id == "Y":  # If YES, collect the Borrower ID
            
            try:
                borrower_id = int(input("What is the borrower's ID number? "))

            except ValueError:
                print("Cannot proceed. Borrower ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function
    
                else:
                    return  # To menu function    

            return borrower_id
                    

        elif know_borrower_id == "N":  # If NO, have the user select from a list of borrowers

            print("Fetching a list of borrowers and their associated IDs for your selection...")   

            borrowers = list_all_borrowers()     

            if not borrowers:  # If no borrowers are found
                print("Cannot proceed as there are no borrowers currently in the database.")
                return  # To the menu function  
                                

            print("Please locate the Borrower ID from the list of borrowers below: ")     
        
            print(f"{'Borrower ID':<5}|{'Name':<25}|{'Email':<40}")
            print("-" * 80)
            for item in borrowers:
                print(f"{item[0]:<5} {item[1]:<25} {item[2]:<40}")  


            try:
                selected_borrower_id = int(input("Please enter the selected Borrower ID: "))                

            except ValueError:
                print("That is not a valid selection. Borrower ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function
                

            # Check that the ID entered by the user matches one of the IDs from the list above
            if not any(borrower[0] == selected_borrower_id for borrower in borrowers):
                print(f"That is not a valid selection. Borrower ID {selected_borrower_id} is not listed above. Please select from the list provided.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            return selected_borrower_id


        else:  # Catches the case where the user does not respond Y/N to knowing the Borrower ID
            print("Cannot proceed. Response for the previous question must be Y or N.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                return  # To menu function    

