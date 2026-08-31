# Library Management System, CLI (Command-Line Interface)

from menu_functions import(
    menu_add_author, menu_add_book, menu_list_all_authors, menu_list_all_books, menu_delete_book,
    menu_add_borrower, menu_list_all_borrowers, menu_update_borrower_email, menu_get_checkouts_by_borrower, menu_get_overdue_books, menu_delete_borrower,
    menu_list_available_books, menu_find_books_by_author, menu_find_books_by_keyword, menu_find_books_by_era, menu_checkout_book, menu_return_book    
)


def main():
    
    while True:
        print(f"\n{'=' * 5} Library Management System {'=' * 5}")

        print(f"\n{'-' * 5} Book Records {'-' * 5}")        
        print("1. List all authors")
        print("2. List all books")
        print("3. Add an author")
        print("4. Add a book")
        print("5. Delete a book")

        print(f"\n{'-' * 5} Borrower Records {'-' * 5}")
        print("6. List all borrowers")              
        print("7. Update a borrower's email address")        
        print("8. View member borrowing activity") 
        print("9. View overdue books") 
        print("10. Add a borrower")  
        print("11. Delete a borrower")

        print(f"\n{'-' * 5} Search, Checkout, & Return {'-' * 5}")
        print("12. List available books")       
        print("13. Search by author")
        print("14. Search by keyword")
        print("15. Search by era")
        print("16. Check out a book")
        print("17. Return a book")
        
        print(f"\n{'-' * 5} Menu Options {'-' * 5}")         
        print("X. Quit")

        choice = input("\nSelect an option (1-17) or X to Quit: ").strip().upper()

        # Book Records
        if choice == "1":
            menu_list_all_authors()
        elif choice == "2":
            menu_list_all_books()        
        if choice == "3":
            menu_add_author()
        elif choice == "4":
            menu_add_book()        
        elif choice == "5":
            menu_delete_book()

        # Borrower Records
        elif choice == "6":
            menu_list_all_borrowers()       
        elif choice == "7":
            menu_update_borrower_email()
        elif choice == "8":
            menu_get_checkouts_by_borrower()
        elif choice == "9":
            menu_get_overdue_books()
        elif choice == "10":
            menu_add_borrower()
        elif choice == "11":
            menu_delete_borrower()

        # Search, Checkout, & Return
        elif choice == "12":
            menu_list_available_books()
        elif choice == "13":
            menu_find_books_by_author()
        elif choice == "14":
            menu_find_books_by_keyword()
        elif choice == "15":
            menu_find_books_by_era()
        elif choice == "16":
            menu_checkout_book()
        elif choice == "17":
            menu_return_book()

        # Exit or Invalid Entry
        elif choice == "X":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number 1-17 or X.")


# BEFORE RUNNING: Ensure that data is seeded via seed_data.py

# Run
if __name__ == "__main__":

    main()