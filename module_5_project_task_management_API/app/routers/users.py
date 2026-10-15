from fastapi import APIRouter, Depends, Request
from app.schemas.user import UserUpdate, UserResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from app.utils.exceptions import DuplicateException, InternalError
from app.utils.security import get_current_user, hash_password
from app.utils.limiter import limiter


router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)


@router.get(
    "/me", 
    response_model=UserResponse,
    responses = {
        200: {"description": "OK - Successfully returned user profile"},      
        401: {"description": "Unauthorized - Invalid or expired token"},
        403: {"description": "Forbidden - User account is inactive"},
        404: {"description": "Not Found - User not found"}  
    }
)
@limiter.limit("60/minute")
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Returns the logged-in user's profile.

    Rate Limit:
    - 60 requests per minute

    1. Utilizes the imported get_current_user function to validate the provided token.
    2. If SUCCESSFUL, returns the user object for the logged-in user.
    3. IF UNSUCCESSFUL, raises an error.

    Standard Response: 
    - 200 - OK (successfully returned the user's profile)
    
    Possible Errors:
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive)
    - 404 - Not Found (the user was not found in the database) 
    """

    return current_user


@router.patch(
    "/me", 
    response_model=UserResponse,
    responses = {
        200: {"description": "OK - Successfully updated the user profile"},      
        401: {"description": "Unauthorized - Invalid or expired token"},
        403: {"description": "Forbidden - User account is inactive"},
        404: {"description": "Not Found - User not found"},
        409: {"description": "Conflict - Unique identifier (email) already exists in the database"},
        422: {"description": "Validation Error - Check request body"},
        500: {"description": "Internal Error - An error occurred while attempting to update the database"}
    }
)
@limiter.limit("30/minute")
def update_profile(
    request: Request,
    user_data: UserUpdate,     
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates a user's profile (email and/or password).  

    Rate Limit:
    - 30 requests per minute  
    
    The request body should contain:
    - **email**: (Optional) The user's new email address (string, must be unique, must be between 7-100 characters and contain '@')
    - **password**: (Optional) The user's new password (string, must be between 8-200 characters)

    1. Utilizes the imported get_current_user function to validate the provided token and return the current user.
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive, raises a 403 error.
    4. If the user cannot be found, raises a 404 error.
    5. If the email is not unique, raises a 409 error.
    6. If other validation constraints are violated, raises a 422 error.
    7. If password is part of the data to be updated, it is hashed before storing in the database.
    8. Attempts to store the submitted updates in the database.
    9. If SUCCESSFUL, returns the updated user profile.
    10. If UNSUCCESSFUL, raises a 500 error.

    Returns:
    - The updated user profile

    Standard Response: 
    - 200 - OK (successfully updated the user's profile)
    
    Possible Errors:
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive)
    - 404 - Not Found (the user was not found in the database) 
    - 409 - Conflict (the email is not unique [already exists in the database])
    - 422 - Validation Error (one or more of the validation requirements has been violated)
    - 500 - Internal Error (an error occurred while attempting to update the user in the database)
    """

    update_data = {
        k: v
        for k, v in user_data.model_dump(exclude_unset=True).items()
        if v is not None
    }

    try:
        for field, value in update_data.items():
            if field == "password":
                value = hash_password(value)
            setattr(current_user, field, value)

        db.commit()
        db.refresh(current_user)

    except IntegrityError:
        db.rollback()
        raise DuplicateException("User", "email", f"{user_data.email}")
    
    except Exception:
        db.rollback()
        raise InternalError(f"Account for User {current_user.id} was not updated.")

    return current_user


@router.delete(
    "/me",
    responses = {
        200: {"description": "OK - Successfully deactivated the user profile"},      
        401: {"description": "Unauthorized - Invalid or expired token"},
        403: {"description": "Forbidden - User account is already deactivated"},
        404: {"description": "Not Found - User not found"},
        500: {"description": "Internal Error - An error occurred while attempting to deactivate the user in the database"}
    }
)       
@limiter.limit("10/minute")
def deactivate_account(
    request: Request,         
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deactivates a user (changes is_active from True to False).

    Rate Limit:
    - 10 requests per minute

    1. Utilizes the imported get_current_user function to validate the provided token and return the current user.
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive, raises a 403 error.
    4. If the user cannot be found, raises a 404 error.
    5. Attempts to deactivate the user in the database.
    6. If SUCCESSFUL, returns a message indicating deactivation was successful.
    7. If UNSUCCESSFUL, raises a 500 error.

    Returns:
    - A success message

    Standard Response: 
    - 200 - OK (successfully deactivated the user's profile)
    
    Possible Errors:
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive)
    - 404 - Not Found (the user was not found in the database) 
    - 500 - Internal Error (an error occurred while attempting to deactivate the user in the database)
    """

    try:
        current_user.is_active = False
        db.commit()        
    
    except Exception:
        db.rollback()
        raise InternalError(f"Account for User {current_user.id} was not deactivated.")

    return {"message": f"Account for User {current_user.id} deactivated successfully."}