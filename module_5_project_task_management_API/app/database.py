from sqlalchemy import create_engine
from app.config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={
        "check_same_thread": False  # Needed for SQLite only
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()

    try:
        yield db  # Provides the database session to the endpoint

    finally:
        db.close()  # Closes session when the request is done