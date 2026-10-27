from app.database import Base, engine, SessionLocal
from app.utils.security import hash_password
from app.config import settings
from app.utils.exceptions import InternalError

# Import models here for SQLAlchemy registration before creating the database tables
from app.models.user import User
from app.models.task import Task
from app.models.activity import ActivityLog


def seed():
    """Creates a sample admin user in order to demonstrate the admin-only endpoint pertaining to activity logs."""

    Base.metadata.create_all(bind=engine)  # Creates database tables if they do not already exist

    sample_admin = User(
        username = "admin_one",
        email = "test_email@test.com",
        hashed_password = hash_password(settings.ADMIN_PASSWORD),
        is_admin = True
    )

    session = SessionLocal()

    try:
        # Check if the admin exists

        existing_admin = (session.query(User).filter_by(username = "admin_one").first())
        
        if existing_admin:
            print("Seeding not needed. Admin already exists in the database.")
            return
        

        # If the admin does not already exist, proceed to add the user to the database

        session.add(sample_admin)
        session.commit()

        print("Data seeded successfully.")    

    except Exception:
        session.rollback()        
        raise InternalError("Data could not be seeded. Please check the database and try again.")        

    finally:
        session.close()   
    

# RUN
if __name__ == "__main__":
    seed()