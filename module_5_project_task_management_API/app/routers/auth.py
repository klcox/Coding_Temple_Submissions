from fastapi import APIRouter, Request, Depends
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.exceptions import DuplicateException, InternalError, UnauthorizedException, ForbiddenException
from app.utils.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.limiter import limiter


router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)


@router.post(
        "/register", 
        response_model=UserResponse, status_code=201,
        responses = {  
            201: {"description": "OK - User created successfully"},      
            409: {"description": "Conflict - Unique identifier (username or email) already exists in the database"},
            422: {"description": "Validation Error - Check request body"},
            500: {"description": "Internal Error - An error occurred while attempting to add the user to the database"}
        }
)
@limiter.limit("5/minute")
def register_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the database. 

    The request body should contain:
    - **username**: (Required) The user's username (string, must be unique, must be between 2-50 characters)
    - **email**: (Required) The user's email address (string, must be between 7-100 characters and contain '@')
    - **password**: (Required) The user's password (string, must be between 8-200 characters)

    1. Verifies whether any unique identifiers (username, email) already exist in the database.
    2. If YES, raises a 409 error.
    3. If NO, attempts to add the new user to the database.
    4. If SUCCESSFUL, returns the new user object.
    5. IF UNSUCCESSFUL, raises a 500 error and rolls back the database to its previous state.  
        
    Returns: 
    - The new user's profile

    Standard Response: 
    - 201 - Created (successfully created the user and added to the database)
    
    Possible Errors:
    - 409 - Conflict (the username and/or email is not unique [already exists in the database])
    - 422 - Validation Error (one or more of the validation requirements has been violated)
    - 500 - Internal Error (an error occurred while attempting to add the user to the database)
    """

    # Check if the user already exists in the database by searching for the unique identifiers (username, email)

    existing_username = db.query(User).filter(User.username == user.username).first()

    if existing_username:
        raise DuplicateException("User", "username", f"{user.username}")

    
    existing_email = db.query(User).filter(User.email == user.email).first()
    
    if existing_email:
        raise DuplicateException("User", "email", f"{user.email}")
    

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
        raise InternalError("User account not created.")

    return new_user


@router.post(
        "/login", 
        response_model=TokenResponse,
        responses = {  
            200: {"description": "OK - User verified successfully, token provided"},      
            401: {"description": "Unauthorized - Username and/or password is incorrect"},
            403: {"description": "Forbidden - User account is inactive"},
            422: {"description": "Validation Error - Check request body"}            
        }
)
@limiter.limit("5/minute")
def login_and_get_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Validates credentials and returns a JWT if verified.
    
    The request body should contain:
    - **username**: (Required) The user's username (string, must be unique, must be between 2-50 characters)  
    - **password**: (Required) The user's password (string, must be between 8-200 characters)

    1. Attempts to locate the user in the database.
    2. If the username and/or password is incorrect, raises a 401 error.
    3. If the user is inactive, raises a 403 error.
    4. If the user is validated successfully, creates and returns a token.      
        
    Returns: 
    - The access token

    Standard Response: 
    - 200 - OK (successfully verified the user's login credentials and returned a token)
    
    Possible Errors:
    - 401 - Unauthorized (the username and/or password could not be verified)
    - 403 - Forbidden (the user account is inactive)
    - 422 - Validation Error (one or more of the validation requirements has been violated)  
    """

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise UnauthorizedException("Incorrect username or password.")

    if not user.is_active:
        raise ForbiddenException("Unable to log-in. Please contact the admin or support.")

    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)