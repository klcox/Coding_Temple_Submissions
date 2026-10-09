from records_books import list_all_authors
from records_borrowers import list_all_borrowers
from search_checkout_return import list_available_books


def retry_or_return():
    """In the event of an error, prompts the user to try again (re-run the function) or to exit the current function. Ultimately, exiting the current function will return to the main menu as handled in menu_functions.py. Returns True if the user would like to try again; returns False if the user would like to exit."""

    while True:

        retry = input("\nPress Y to try again or N to return to the main menu. ").strip().upper()

        if retry == "Y":
           return True  # Re-runs the associated function loop

        elif retry == "N":
            return False # Exits the associated function loop

        else:
            print("\nThat is not a valid selection. Response for the previous question must be Y or N.")  # Continues the loop until a valid response is received


def collect_author_id():
    """Determines how the user would like to provide the Author ID - either directly or by selecting from a list. Collects and returns the Author ID. Returns None if there are no Authors in the database or if the user chooses to exit."""

    while True:

        # Check if the user knows the Author ID
        know_author_id = input("\nDo you know the Author ID number? (Y/N) ").strip().upper()

        if know_author_id == "Y":  # If YES, collect the Author ID
                      
            try:
                author_id = int(input("\nWhat is the author's ID number? ").strip())               

            except ValueError:
                print("\nThat is not a valid entry. Author ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            return author_id
        

        elif know_author_id == "N":  # If NO, have the user select from a list of authors
                    
            print("\nFetching a list of authors and their associated IDs for your selection...")        

            authors = list_all_authors()  

            if not authors:  # If no authors are found
                print("\nCannot proceed as there are no authors currently in the database.")
                return  # To the menu function  
                                

            print("\nPlease locate the Author ID from the list of authors below:\n")       
            print(f"{'ID':<5} | {'Author Name':<25} | {'Bio':<25}")
            print("-" * 60)
            for item in authors:
                bio = item[2]
                
                if len(bio) > 20:
                    bio = bio[:20] + "..."
                print(f"{item[0]:<5} | {item[1]:<25} | {bio:<25}") 


            try:
                selected_author_id = int(input("\nPlease enter the selected Author ID: ").strip())        

            except ValueError:
                print("\nThat is not a valid selection. Author ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function
                

            # Check that the ID entered by the user matches one of the IDs from the list above
            if not any(author[0] == selected_author_id for author in authors):
                print(f"\nThat is not a valid selection. Author ID {selected_author_id} is not listed above. Please select from the list provided.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            return selected_author_id


        else:  # Catches the case where the user does not respond Y/N to knowing the Author ID
            print("\nThat is not a valid selection. Response for the previous question must be Y or N.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                return  # To menu function  
            

def collect_book_id():
    """Determine how the user would like to provide the Book ID - either directly or by selecting from a list of available books. Collects and returns the Book ID. Returns None if there are no Books in the database or if the user chooses to exit."""

    while True:

        # Check if the user knows the Book ID 
        know_book_id = input("\nDo you know the Book ID number? (Y/N) ").strip().upper()

        if know_book_id == "Y":  # If YES, collect the Book ID
            
            try:
                book_id = int(input("\nWhat is the book's ID number? ").strip())

            except ValueError:
                print("\nThat is not a valid entry. Book ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function
    
                else:
                    return  # To menu function    

            return book_id
                 

        elif know_book_id == "N":  # If NO, have the user select from a list of available books

            print("\nFetching a list of available books and their associated IDs for your selection...")   

            books = list_available_books()     

            if not books:  # If no books are found
                print("\nCannot proceed as no books are currently available.")
                return  # To the menu function  
                                

            print("\nPlease locate the Book ID from the list of books below:\n")        
            print(f"{'ID':<5} | {'Title':<40} | {'Author(s)':<40} | {'ISBN':<20} | {'Year Originally Published':<30} | {'Available Copies':<20}")
            print("-" * 167)
            for item in books:
                print(f"{item[0]:<5} | {item[1]:<40} | {item[2]:<40} | {item[3]:<20} | {item[4]:<30} | {item[5]:<20}") 


            try:
                selected_book_id = int(input("\nPlease enter the selected Book ID: ").strip())                

            except ValueError:
                print("\nThat is not a valid selection. Book ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function
                

            # Check that the ID entered by the user matches one of the IDs from the list above
            if not any(book[0] == selected_book_id for book in books):
                print(f"\nThat is not a valid selection. Book ID {selected_book_id} is not listed above. Please select from the list provided.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            return selected_book_id


        else:  # Catches the case where the user does not respond Y/N to knowing the Book ID
            print("\nThat is not a valid selection. Response for the previous question must be Y or N.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                return  # To menu function      


def collect_borrower_id():
    """Determine how the user would like to provide the Borrower ID - either directly or by selecting from a list. Collects and returns the Borrower ID. Returns None if there are no Borrowers in the database or if the user chooses to exit."""

    while True:

        # Check if the user knows the Borrower ID 
        know_borrower_id = input("\nDo you know the Borrower ID number? (Y/N) ").strip().upper()

        if know_borrower_id == "Y":  # If YES, collect the Borrower ID
            
            try:
                borrower_id = int(input("\nWhat is the borrower's ID number? ").strip())

            except ValueError:
                print("\nThat is not a valid entry. Borrower ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function
    
                else:
                    return  # To menu function    

            return borrower_id
                    

        elif know_borrower_id == "N":  # If NO, have the user select from a list of borrowers

            print("\nFetching a list of borrowers and their associated IDs for your selection...")   

            borrowers = list_all_borrowers()     

            if not borrowers:  # If no borrowers are found
                print("\nCannot proceed as there are no borrowers currently in the database.")
                return  # To the menu function  
                                

            print("\nPlease locate the Borrower ID from the list of borrowers below:\n")             
            print(f"{'ID':<5} | {'Name':<25} | {'Email':<30} | {'Phone':<15} | {'Membership Date':<15}")
            print("-" * 103)
            for item in borrowers:
                print(f"{item[0]:<5} | {item[1]:<25} | {item[2]:<30} | {item[3]:<15} | {str(item[4]):<15}") 


            try:
                selected_borrower_id = int(input("\nPlease enter the selected Borrower ID: ").strip())                

            except ValueError:
                print("\nThat is not a valid selection. Borrower ID must be an integer.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function
                

            # Check that the ID entered by the user matches one of the IDs from the list above
            if not any(borrower[0] == selected_borrower_id for borrower in borrowers):
                print(f"\nThat is not a valid selection. Borrower ID {selected_borrower_id} is not listed above. Please select from the list provided.")

                if retry_or_return():
                    continue  # Re-run the function

                else:
                    return  # To menu function

            return selected_borrower_id


        else:  # Catches the case where the user does not respond Y/N to knowing the Borrower ID
            print("\nThat is not a valid selection. Response for the previous question must be Y or N.")

            if retry_or_return():
                continue  # Re-run the function

            else:
                return  # To menu function    

