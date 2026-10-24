from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.exceptions import DuplicateError, InternalError, InvalidAuthError
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Creates a new user in the database. Returns the new user's profile."""

    # Check if the user already exists in the database by searching for the unique identifiers (username, email)

    existing_username = db.query(User).filter(User.username == user.username).first()

    if existing_username:
        raise DuplicateError("Cannot create account. A user with this username already exists.")

    
    existing_email = db.query(User).filter(User.email == user.email).first()
    
    if existing_email:
        raise DuplicateError("Cannot create account. A user with this email address already exists.")
    

    # If the user does not already exist, proceed to create the user and add to the database
    
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hash_password(user.password)
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception:
        db.rollback()
        raise InternalError("Cannot create account. An internal server error occurred.")

    return new_user


@router.post("/token", response_model=TokenResponse)
def login_and_get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Validates credentials and returns a JWT if verified."""

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise InvalidAuthError("Incorrect username or password.")

    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Returns the authenticated user's details."""

    return current_user


@router.get("/profile", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Returns the authenticated user's profile."""

    return current_user