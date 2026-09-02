from sqlalchemy import create_engine, Integer, String, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional
from datetime import date

engine = create_engine("sqlite:///library.db", echo=False)


class Base(DeclarativeBase):
    pass


# Association table for Books & Authors
books_authors = Table(
    "books_authors",
    Base.metadata,
    Column("book_id",  Integer, ForeignKey("books.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
 )


class Author(Base):
    __tablename__ = "authors"

    # Fundamental attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500))

    # Relationship to Books
    books: Mapped[list["Book"]] = relationship(secondary=books_authors, back_populates="authors")

    def __repr__(self):
        bio = self.bio if self.bio is not None else "N/A"
        return f"Author(id='{self.id}', name='{self.name}', bio='{bio}')"


class Book(Base):
    __tablename__ = "books"

    # Fundamental attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    isbn: Mapped[str] = mapped_column(String(13), unique=True, nullable=False)
    year_published: Mapped[int] = mapped_column(nullable=False)  # Refers to the original publication date, not specific to this version
    era: Mapped[str] = mapped_column(nullable=False)  # BCE or CE based on the year of publication
    available_copies: Mapped[int] = mapped_column(nullable=False, default=1)

    # Relationships to Authors, Checkouts
    authors: Mapped[list["Author"]] = relationship(secondary=books_authors, back_populates="books")    
    checkouts: Mapped[list["Checkout"]] = relationship(back_populates="book")
    
    def __repr__(self):
        return f"Book(id='{self.id}', title='{self.title}', isbn='{self.isbn}', year_published={abs(self.year_published)} {self.era}, available_copies={self.available_copies})"


class Borrower(Base):
    __tablename__ = "borrowers"

    # Fundamental attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email_address: Mapped[str] = mapped_column(unique=True, nullable=False)    
    membership_date: Mapped[date] = mapped_column(nullable=False)
    phone: Mapped[Optional[str]] = mapped_column()

    # Relationship to Checkouts    
    checkouts: Mapped[list["Checkout"]] = relationship(back_populates="borrower")

    def __repr__(self):
        phone = self.phone if self.phone is not None else "N/A"
        return f"Borrower(id='{self.id}', name='{self.name}', email='{self.email_address}', phone='{phone}', membership_date='{self.membership_date}')"


class Checkout(Base):
    __tablename__ = "checkouts"

    # Fundamental attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    checkout_date: Mapped[date] = mapped_column(nullable=False)
    due_date: Mapped[date] = mapped_column(nullable=False)
    return_date: Mapped[Optional[date]] = mapped_column()  # Optional/nullable as return_date would be set later via a separate function rather than at checkout creation

    # Relationships to Books, Borrowers
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    book: Mapped["Book"] = relationship(back_populates="checkouts")

    borrower_id: Mapped[int] = mapped_column(ForeignKey("borrowers.id"))
    borrower: Mapped["Borrower"] = relationship(back_populates="checkouts")

    def __repr__(self):
        return_date = self.return_date if self.return_date is not None else "N/A"
        return f"Checkout(id='{self.id}', checkout_date={self.checkout_date}, due_date={self.due_date}, return_date={return_date})"


def init_db():
    """Create all database tables. Call this before using any other functions."""
    Base.metadata.create_all(engine)