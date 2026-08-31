from models import init_db
from records_books import(add_author, add_book)
from records_borrowers import(add_borrower)
from search_checkout_return import(checkout_book)
from datetime import date, timedelta

def seed():
    init_db()  # Initialize the database by creating the tables for Author, Book, Borrower, and Checkout
    print("Database initialized.")

    # Add beginning data to run/test the library management system   
    tolkien = add_author("J.R.R. Tolkien")
    applegate  = add_author("K. A. Applegate")
    dickens = add_author("Charles Dickens", "Classical author")
    fitzgerald = add_author("F. Scott Fitzgerald", "Classical author")
    sun_tzu = add_author("Sun Tzu")
    bernstein = add_author("Carl Bernstein", "Journalist for the Washington Post")
    woodward = add_author("Bob Woodward", "Journalist for the Washington Post")


    add_book("The Fellowship Of The Ring", "9780547928210", 1954, author_ids=[tolkien.id])
    add_book("The Two Towers", "9780547928203", 1954, author_ids=[tolkien.id])
    add_book("The Return of the King", "9780547928197", 1955, author_ids=[tolkien.id])
    add_book("Remnants: The Mayflower Project", "9780439544092", 2001, author_ids=[applegate.id])
    add_book("A Tale of Two Cities", "9781454957546", 1859, available_copies=3, author_ids=[dickens.id])
    add_book("The Great Gatsby", "9781441341693", 1925, author_ids=[fitzgerald.id])
    add_book("The Art of War", "9789386538215", -450, author_ids=[sun_tzu.id])
    add_book("All the President's Men", "9781416527572", 1974, author_ids=[bernstein.id, woodward.id])


    add_borrower("Alice Chen", "alice@example.com", "123-456-7890")
    add_borrower("Bob Martinez", "bob@example.com")
    add_borrower("Charlie Jackson", "charlie@example.com", "(098) 765-4321")
    add_borrower("David Michaels", "dave@example.com")
    add_borrower("Eddie Lancaster", "eddie@example.com")
    

    yesterday = date.today() - timedelta(days=1)
    checkout_book(1, 1, checkout_date=yesterday)  # The Fellowship Of The Ring, Alice, Checkout Date is Yesterday
    checkout_book(2, 1)  # The Two Towers, Alice, Checkout Date is Today
    checkout_book(3, 3)  # The Return of the King, Charlie, Checkout Date is Today
    checkout_book(4, 2, checkout_date=yesterday)  # Remnants: The Mayflower Project, Bob, Checkout Date is Yesterday
    checkout_book(5, 5)  # A Tale of Two Cities, Eddie, Checkout Date is Today
    checkout_book(6, 5)  # The Great Gatsby, Eddie, Checkout Date is Today

    print("Seed data added.")


# Run
if __name__ == "__main__":
    seed()