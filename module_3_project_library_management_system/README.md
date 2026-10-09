# Library Management System
This project mimics a library management system, utilizing Python and SQLAlchemy to create and enable the user to interact with a database (library.db) via a CLI.

## Database Design
The database consists of (4) underlying models: Author, Book, Borrower, and Checkout.

- Author and Book have a many-to-many relationship such that one author can write multiple books, and one book can have more than one author. 

- Book and Checkout have a one-to-many relationship: a book may be checked out more than once over time, but there is only one book per checkout. (I decided not to implement multiple books per checkout so as to preserve the integrity of the checkout object, for simplicity and ease of use, and in that some books may have different checkout durations.)

- Borrower and Checkout similarly have a one-to-many relationship: a borrower may make multiple checkouts, but there is only one borrower per checkout.

### ERD Visualization:
(Attributes are required/non-nullable unless otherwise specified)

    [Author]         <----->         [Book]                              ----->        [Checkout]
    PK id                            PK id                                             PK id
    name                             title                                             checkout_date
    bio (optional)                   isbn (unique)                                     due_date
                                     year_published                                    return_date (optional because it is assigned through a later function, not at Checkout creation)
    |                                era (assigned based on year_published)            FK book_id
    |                                available_copies (default = 1)                    FK borrower_id
    |
    |                                |                                                 ^
    |                                |                                                 |
    |                                |                                                 |
    |                                |
    ->     [Association Table]      <-                                                 [Borrower] 
            FK book_id                                                                 PK id
            FK author_id                                                               name
                                                                                       email_address (unique)
                                                                                       membership_date
                                                                                       phone (optional)

## Project Structure
| File | Purpose | Contents
|---|---|---|
| `models.py` | Establishes the models and relationships noted above | `Author`, `Book`, `Borrower`, `Checkout` |
| `records_books.py` | Underlying functions related to books and authors | `list_all_authors`, `list_all_books`, `add_author`, `add_book`, `delete_book` |
| `records_borrowers.py` | Underlying functions related to borrowers | `list_all_borrowers`, `update_borrower_email`, `get_checkouts_by_borrower`, `get_overdue_books`, `add_borrower`, `delete_borrower`, and any helper functions |
| `search_checkout_return.py` | Underlying functions related to searches, checkouts, and returns | `list_available_books`, `find_books_by_author`, `find_books_by_keyword`, `find_books_by_era`, `checkout_book`, `return_book` |
| `seed_data.py` | Initializes the database (creates the tables) and adds seed data | Seed data (various authors, books, borrowers, and checkouts) to enable a user to test the database |
| `menu_functions.py` | Menu functions which translate/pass user input to the underlying functions | Naming follows the convention of `menu_` + function name above |
| `helper_menu_functions.py` | Functions that assist in directing the flow of the menu and collecting user input; separated for readability | `retry_or_return`, `collect_author_id`, `collect_book_id`, `collect_borrower_id` |
| `main.py` | CLI | 17 menu options, along with the option to exit the program |

## Validation/Error Handling
The project is designed so that there is a separation of responsibilities between underlying functions and menu functions.

### Underlying Functions
- conduct data validation (e.g. empty strings, email and phone format, 13-digit ISBNs, preventing available copies from becoming negative, ensuring IDs exist, etc.)
- perform the database operation (addition, deletion, updating data, producing a list)
- print operation-specific confirmation/error messages

### Menu Functions
- collect user input
- conduct light type validation for user-friendliness (e.g. ensuring the year_published gets passed to the underlying function as an integer to prevent invalid/uninformative error messages)
- display list results to the user (e.g. authors, books, borrower activity)
- handle menu flow (retries/redirection back to the CLI)

## Future Features:
- Additional retry/return options for improved user-friendliness
- Functions to update most other aspects of each model (e.g. Author name, Book title, Borrower phone, etc.)
- Functions to search Borrowers and find a Book by its ISBN
- Allow the user to choose how the results are sorted in the display
- Deactivate Authors, Books, and Borrowers rather than deleting them so as to preserve historical records
- Functions to retrieve all Checkout history, current Checkouts, and Checkout history by book
- Functions to export database information to a CSV file
- Convert database records to pandas DataFrames for further analysis and reporting

## Special Note
`seed_data.py` is intended to be run with a **fresh** database so as to initialize the library with sample data for testing. Running this file multiple times on an existing database may result in duplicate records or constraint errors. If the latter occurs, delete `library.db` and the `__pycache__` folder; then try running `seed_data.py` again.

## Setup
1. Clone this repo
2. Create a virtual environment (e.g. for Windows/Git Bash: `python -m venv venv`)
3. Activate the virtual environment (e.g. for Windows/Git Bash: `source venv/Scripts/activate`)
4. Install sqlalchemy (e.g. for Windows/Git Bash: `pip install sqlalchemy`)
5. Initialize the database and add the seed data: `python seed_data.py`
6. Run the CLI: `python main.py`
