from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite only
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # bind=engine connects the session to the engine

class Base(DeclarativeBase):
    pass

def get_db():
    """Dependency that provides a database session per request."""

    db = SessionLocal()

    try:
        yield db  # Give the session to the endpoint

    finally:
        db.close()  # Close the session when the request is done