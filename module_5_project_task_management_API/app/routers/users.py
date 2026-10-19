from fastapi import APIRouter, Request, Depends, Query
from app.schemas.user import UserUpdate, UserResponse
from app.utils.limiter import limiter
from app.models.user import User
from app.utils.security import get_current_user, hash_password, verify_admin_status
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import IntegrityError
from app.utils.exceptions import DuplicateException, InternalError, BadRequestException

from app.models.activity import ActivityLog
from app.schemas.activity import ActivityLogResponse
from app.enums import ActivityLogAction
from typing import Optional
from datetime import datetime


router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)


# ===========
# GET PROFILE
# ===========


@router.get(
    "/me", 
    response_model=UserResponse,
    responses = {
        200: {"description": "OK - Successfully returned user profile"},
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from get_current_user
        403: {"description": "Forbidden - User account is inactive"}  # Stems from get_current_user
    }
)
@limiter.limit("60/minute")
def get_profile(request: Request, current_user: User = Depends(get_current_user)):
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
    """

    return current_user


# ==============
# UPDATE PROFILE
# ==============


@router.patch(
    "/me", 
    response_model=UserResponse,
    responses = {
        200: {"description": "OK - Successfully updated the user profile"},      
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from get_current_user
        403: {"description": "Forbidden - User account is inactive"},  # Stems from get_current_user   
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
    4. If the email is not unique, raises a 409 error.
    5. If other validation constraints are violated, raises a 422 error.
    6. If password is part of the data to be updated, it is hashed before storing in the database.
    7. Attempts to store the submitted updates in the database.
    8. If SUCCESSFUL, returns the updated user profile.
    9. If UNSUCCESSFUL, raises a 500 error.

    Returns:
    - The updated user profile

    Standard Response: 
    - 200 - OK (successfully updated the user's profile)
    
    Possible Errors:
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive)    
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


# ==============
# DELETE PROFILE
# ==============


@router.delete(
    "/me",
    responses = {
        200: {"description": "OK - Successfully deactivated the user profile"},      
        401: {"description": "Unauthorized - Invalid or expired token"},
        403: {"description": "Forbidden - User account is already deactivated"},        
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
    4. Attempts to deactivate the user in the database.
    5. If SUCCESSFUL, returns a message indicating deactivation was successful.
    6. If UNSUCCESSFUL, raises a 500 error.

    Returns:
    - A success message

    Standard Response: 
    - 200 - OK (successfully deactivated the user's profile)
    
    Possible Errors:
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive)    
    - 500 - Internal Error (an error occurred while attempting to deactivate the user in the database)
    """

    try:
        current_user.is_active = False
        db.commit()        
    
    except Exception:
        db.rollback()
        raise InternalError(f"Account for User {current_user.id} was not deactivated.")

    return {"message": f"Account for User {current_user.id} deactivated successfully."}


# =================
# GET ACTIVITY LOGS
# =================


@router.get(
    "/activity", 
    response_model=list[ActivityLogResponse],
    responses = {
        200: {"description": "OK - Successfully returned activity logs"},
        400: {"description": "Bad Request - Query parameter error pertaining to start_date and/or end_date"},
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from verify_admin_status (and then get_current_user)
        403: {"description": "Forbidden - User account is inactive or not an admin"},  # Stems from verify_admin_status (and then get_current_user),
        422: {"description": "Validation Error - Check the query parameter constraints"}
    }
)
@limiter.limit("60/minute")
def get_activity_logs(
    request: Request,
    user_id: Optional[int] = Query(default=None, gt=0, description="Filter by specific user"),
    action: Optional[ActivityLogAction] = Query(default=None, description="Filter by action"),
    start_date: datetime = Query(default="2026-01-01T00:00:00", description="Filter by date (start)"),
    end_date: datetime = Query(default="2100-01-01T00:00:00", description="Filter by date (end)"),
    search: Optional[str] = Query(default=None, min_length=1, max_length=200, description="Search task title"),    
    skip: int = Query(default=0, ge=0, description="Number of activity logs to skip for pagination"),
    limit: int = Query(default=10, ge=1, le=20, description="Max number of results for pagination"),
    db: Session = Depends(get_db), 
    admin_user: User = Depends(verify_admin_status)
):
    """
    ADMIN ONLY endpoint. 

    Returns user activity logs.
    
    Rate Limit:
    - 60 requests per minute

    Includes options for filtering by:
    - user_id: value must be greater than zero
    - action: one of "created", "updated", "deleted"
    - start_date and/or end_date: must be no earlier than "2026-01-01T00:00:00" and no later than "2100-01-01T00:00:00"
    - search: (task title content) must be between 1 and 200 characters

    Includes options for pagination
    - skip: number of activity logs to skip
    - limit: max number of results to display per page  
    
    1. Utilizes the imported verify_admin_status function to validate the provided token as well as admin status and return the current user.
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive or if the user does not have admin status, raises a 403 error.
    4. Searches the database for activity logs according to query parameters as necessary.
    5. If the query parameter is invalid or inconsistent (e.g. an end_date earlier than a start_date), raises a 400 error.
    6. If one or more validation constraints has been violated, raises a 422 error.
    7. Otherwise, returns the associated activity logs.  
      
    Standard Response: 
    - 200 - OK (successfully returned activity logs)
    
    Possible Errors:
    - 400 - Bad Request (query parameter error)
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive or does not have admin status)
    - 422 - Validation Error (one or more of the validation requirements has been violated)  
    """ 

    query = db.query(ActivityLog)


    # Filtering

    if user_id is not None:
        query = query.filter(ActivityLog.user_id == user_id)

    if action is not None:
        query = query.filter(ActivityLog.action == action) 

    if end_date < start_date:  # If end_date occurs before start_date
        raise BadRequestException("End date must occur on or after start date.")

    if start_date < datetime(2026, 1, 1):  # If start_date is earlier than default min
        raise BadRequestException("Start date must occur on or after 2026-01-01.")

    if end_date > datetime(2100, 1, 1):  # If end_date is later than default max
        raise BadRequestException("End date must occur on or before 2100-01-01.")

    query = query.filter(ActivityLog.timestamp >= start_date, ActivityLog.timestamp <= end_date)

    if search is not None:
        query = query.filter(ActivityLog.task_title.ilike(f"%{search}%"))


    # Ordering

    query = query.order_by(ActivityLog.timestamp.desc())  # Displays newest logs first


    # Pagination
    
    query = query.offset(skip).limit(limit)


    logs = query.all()
    return logs