from fastapi import APIRouter, Request, Depends, Query
from app.schemas.user import UserUpdate, UserResponse
from app.utils.limiter import limiter
from app.models.user import User
from app.utils.security import get_current_user, hash_password, verify_admin_status
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import IntegrityError
from app.utils.exceptions import DuplicateException, InternalError, NotFoundException, BadRequestException

from app.schemas.activity import ActivityLogPaginationResponse
from app.models.activity import ActivityLog
from typing import Optional
from app.utils.enums import ActivityLogAction
from datetime import datetime
import math


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
        200: {"description": "OK - Successfully returned user's profile"},
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
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive, raises a 403 error. 
    4. If the token is validated successfully, returns the user object for the logged-in user.

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
        200: {"description": "OK - Successfully updated the user's profile"},
        400: {"description": "Bad Request - Request is empty"},    
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
    4. If the request is empty, raises a 400 error.
    4. If a new email is provided but is not unique, raises a 409 error.
    5. If other validation constraints are violated, raises a 422 error.
    6. If a new password is provided, it is hashed before storing in the database.
    7. Attempts to store the submitted updates in the database.
    8. If SUCCESSFUL, returns the updated user profile.
    9. If UNSUCCESSFUL, raises a 500 error and rolls back the database to its previous state.

    Returns:
    - The updated user profile

    Standard Response: 
    - 200 - OK (successfully updated the user's profile)
    
    Possible Errors:
    - 400 - Bad Request (the request is empty)
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive)    
    - 409 - Conflict (the email is not unique [already exists in the database])
    - 422 - Validation Error (one or more of the validation requirements has been violated)
    - 500 - Internal Error (an error occurred while attempting to update the user in the database)
    """

    update_data = {  # Gather only the submitted values and ensure they are not None
        k: v
        for k, v in user_data.model_dump(exclude_unset=True).items()
        if v is not None
    }

    if not update_data:
        raise BadRequestException("No fields provided to update.")

    try:
        for field, value in update_data.items():
            if field == "password":
                current_user.hashed_password = hash_password(value)
            else:
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


# ===========================
# DELETE (DEACTIVATE) PROFILE
# ===========================


@router.delete(
    "/me",
    responses = {
        200: {"description": "OK - Successfully deactivated the user profile"},      
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from get_current_user
        403: {"description": "Forbidden - User account is already deactivated"},  # Stems from get_current_user  
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
    3. If the user account is already deactivated, raises a 403 error.    
    4. Attempts to deactivate the user in the database.
    5. If SUCCESSFUL, returns a message indicating deactivation was successful.
    6. If UNSUCCESSFUL, raises a 500 error and rolls back the database to its previous state.

    Returns:
    - A success message

    Standard Response: 
    - 200 - OK (successfully deactivated the user's profile)
    
    Possible Errors:
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is already deactivated)    
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
    response_model=ActivityLogPaginationResponse,
    responses = {
        200: {"description": "OK - Successfully returned activity logs"},
        400: {"description": "Bad Request - Business rule violation"},
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from verify_admin_status (and then get_current_user)
        403: {"description": "Forbidden - User account is inactive or not an admin"},  # Stems from verify_admin_status (and then get_current_user)
        404: {"description": "Not Found - user_id provided as a query parameter not found"},
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
    page: int = Query(default=1, ge=1, description="On which page to begin for pagination results"),
    limit: int = Query(default=10, ge=1, le=20, description="Max number of results per page"),    
    admin_user: User = Depends(verify_admin_status),
    db: Session = Depends(get_db)
):
    """
    ADMIN ONLY endpoint. 

    Returns user activity logs.
    
    Rate Limit:
    - 60 requests per minute

    Includes options for filtering by:
    - user_id: value must be greater than zero; default is None
    - action: one of "created", "updated", "deleted"; default is None
    - start_date and/or end_date: must be no earlier than "2026-01-01T00:00:00" and no later than "2100-01-01T00:00:00"
    - search: (task title content) must be between 1 and 200 characters; default is None

    Includes options for pagination:
    - page: on which page to begin the results; default is 1
    - limit: max number of results to display per page; default is 10
    
    1. Utilizes the imported verify_admin_status function to validate the provided token as well as admin status and return the current user.
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive or if the user does not have admin status, raises a 403 error.
    4. Searches the database for activity logs according to query parameters as necessary.
    5. If the user_id provided as a query parameter is not found, raises a 404 error.
    6. If a business rule has been violated (e.g. an end_date earlier than a start_date), raises a 400 error.
    7. If one or more validation constraints has been violated, raises a 422 error.
    8. Otherwise, returns the associated activity logs.  
      
    Standard Response: 
    - 200 - OK (successfully returned activity logs)
    
    Possible Errors:
    - 400 - Bad Request (business rule violation)
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive or does not have admin status)
    - 404 - Not Found (the user ID provided as a query parameter was not found)
    - 422 - Validation Error (one or more of the validation requirements has been violated)  
    """ 

    query = db.query(ActivityLog)


    # Filtering

    if user_id is not None:

        user = db.query(User).filter(User.id == user_id).first()  # First check whether the user exists
        if user is None:     
            raise NotFoundException("User", f"ID {user_id}")  

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


    # Metadata Calculation

    total_logs = query.count()

    if total_logs == 0:  # If there are no logs to display
        return {
            "data": [],
            "meta": {
                "total": 0,
                "num_pages": 1,
                "page": 1,
                "limit": limit
            }
        }

    num_pages = math.ceil(total_logs / limit)  # If the division results exceed a whole number (e.g. 3.1), round up to the next whole number (e.g. 3.1 becomes 4)

    if page > num_pages and total_logs > 0:  # If there are log results but the requested page exceeds the available pages to display
        raise BadRequestException(f"Page must be between 1 and {num_pages}.")
    

    # Ordering
    
    query = query.order_by(ActivityLog.timestamp.desc(), ActivityLog.id.desc())  # Displays newest logs first, with a secondary ordering by log ID in the event of a duplicate timestamp


    # Pagination
    
    skip = (page - 1) * limit
    
    logs = query.offset(skip).limit(limit).all()


    return {
        "data": logs,
        "meta": {
            "total": total_logs,
            "num_pages": num_pages,
            "page": page,
            "limit": limit
        }
    }