from fastapi import APIRouter, Request, Depends, Query, Path, BackgroundTasks
from app.models.activity import ActivityLog
from app.database import get_db, SessionLocal
from app.utils.exceptions import InternalError, NotFoundException, ForbiddenException, BadRequestException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskPaginationResponse
from app.utils.limiter import limiter
from app.utils.security import get_current_user
from typing import Optional
from app.utils.enums import TaskPriority, TaskSort, TaskSortOrder
import math
from sqlalchemy import case


router = APIRouter(
    prefix = "/tasks",
    tags = ["Tasks"]
)


# ================
# HELPER FUNCTIONS
# ================


def create_activity_log(user_id: int, task_id: int, task_title: str, action: str, changes: str = None):  
    """Background task - creates in the database an activity log associated with the logged-in user and a specific task."""     
    
    new_log = ActivityLog(
        user_id = user_id,
        task_id = task_id,
        task_title = task_title,
        action = action,
        changes = changes
    )

    db = SessionLocal()

    try:
        db.add(new_log)
        db.commit()          

    except Exception:  # Background task exception may be logged by the server but will not change the primary response already returned to the client
        db.rollback()
        raise InternalError("Task was not logged.")

    finally: 
        db.close()


def get_task_or_raise(task_id: int, db: Session, current_user: User):
    """Helper function - attempts to locate a specific task in the database. Returns the task if successful; otherwise, raises an error."""

    task = db.query(Task).filter(Task.id == task_id).first()
        
    if not task:
        raise NotFoundException("Task", f"ID {task_id}")

    if task.user_id != current_user.id:
        raise ForbiddenException("You do not have permission to access this task.")

    return task


# ===========
# CREATE TASK
# ===========


@router.post(
    "/", 
    response_model=TaskResponse, 
    status_code=201,
    responses = {
        201: {"description": "Created - Task created successfully"}, 
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from get_current_user
        403: {"description": "Forbidden - User account is inactive"},  # Stems from get_current_user
        422: {"description": "Validation Error - Check request body"},
        500: {"description": "Internal Error - An error occurred while attempting to add the task to the database"}
    }
)
@limiter.limit("30/minute")
def create_task(
    request: Request,
    background_tasks: BackgroundTasks,
    task: TaskCreate,         
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Creates a new task for the logged-in user.

    Rate Limit:
    - 30 requests per minute  
    
    The request body should contain:
    - **title**: (Required) The task title (string, must be between 1-200 characters)
    - **description**: (Optional) The task description (string, must be between 1-2000 characters; default is None)
    - **priority**: (Optional) The task priority level (one of "low", "medium", "high", "urgent"; default is "medium")

    1. Utilizes the imported get_current_user function to validate the provided token and return the current user.
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive, raises a 403 error.        
    4. If any validation constraints are violated, raises a 422 error.    
    5. Otherwise, attempts to create the task and add it to the database.
    6. If SUCCESSFUL, returns the new task object. (**Background task**: creates an activity log for this user/task.)
    7. If UNSUCCESSFUL, raises a 500 error and rolls back the database to its previous state.

    Returns:
    - The created task object

    Standard Response: 
    - 201 - Created (successfully created the new task and added to the database)
    
    Possible Errors:
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive)        
    - 422 - Validation Error (one or more of the validation requirements has been violated)
    - 500 - Internal Error (an error occurred while attempting to add the task to the database)
    """

    new_task = Task(**task.model_dump(), user_id=current_user.id)

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)   

    except Exception:  
        db.rollback()
        raise InternalError("New task was not created.")
    
    background_tasks.add_task(create_activity_log, current_user.id, new_task.id, new_task.title, action="created")
    return new_task


# =============
# GET ALL TASKS
# =============


@router.get(
    "/", 
    response_model=TaskPaginationResponse,
    responses = {
        200: {"description": "OK - Successfully returned tasks"},
        400: {"description": "Bad Request - Business rule violation"},
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from get_current_user
        403: {"description": "Forbidden - User account is inactive"},  # Stems from get_current_user
        422: {"description": "Validation Error - Check the query parameter constraints"}
    }
)
@limiter.limit("60/minute")
def get_all_tasks(
    request: Request,
    completed: Optional[bool] = Query(default=None, description="Filter by completion status"),
    priority: Optional[TaskPriority] = Query(default=None, description="Filter by priority"),
    search: Optional[str] = Query(default=None, min_length=1, max_length=200, description="Search task title"),
    sort_by: TaskSort = TaskSort.priority,
    sort_order: TaskSortOrder = TaskSortOrder.desc,
    page: int = Query(default=1, ge=1, description="On which page to begin for pagination results"),
    limit: int = Query(default=10, ge=1, le=20, description="Max number of results per page"),     
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns tasks for the logged-in user.
        
    Rate Limit:
    - 60 requests per minute

    Includes options for filtering by:
    - completed: boolean; default is None
    - priority: one of "low", "medium", "high", "urgent"; default is None  
    - search: (task title content) must be between 1 and 200 characters; default is None

    Includes options for sorting:
    - sort_by: one of "created_at", "title", "completed", "priority"; default is "priority"
    - sort_order: one of "asc" (for ascending) or "desc" (for descending); default is "desc"

    Includes options for pagination:
    - page: on which page to begin the results; default is 1
    - limit: max number of results to display per page; default is 10
    
    1. Utilizes the imported get_current_user function to validate the provided token and return the current user.
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive, raises a 403 error.
    4. Searches the database for the logged-in user's tasks according to query parameters as necessary.
    5. If a business rule has been violated (e.g. page is greater than the number of pages returned), raises a 400 error.
    6. If one or more validation constraints has been violated, raises a 422 error.
    7. Otherwise, returns the associated tasks.  
        
    Standard Response: 
    - 200 - OK (successfully returned tasks)
    
    Possible Errors:
    - 400 - Bad Request (business rule violation)
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive)    
    - 422 - Validation Error (one or more of the validation requirements has been violated)  
    """

    query = db.query(Task).filter(Task.user_id == current_user.id)


    # Filtering

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    if search is not None:
        query = query.filter(Task.title.ilike(f"%{search}%"))


    # Metadata Calculation

    total_tasks = query.count()

    if total_tasks == 0:  # If there are no tasks to display
        return {
            "data": [],
            "meta": {
                "total": 0,
                "num_pages": 1,
                "page": 1,
                "limit": limit
            }
        }

    num_pages = math.ceil(total_tasks / limit)  # If the division results exceed a whole number (e.g. 3.1), round up to the next whole number (e.g. 3.1 becomes 4)

    if page > num_pages and total_tasks > 0:  # If there are task results but the requested page exceeds the available pages to display
        raise BadRequestException(f"Page must be between 1 and {num_pages}.")
    

    # Sorting    

    if sort_by == TaskSort.priority:
        sort_column = case(
            (Task.priority == TaskPriority.urgent, 4),
            (Task.priority == TaskPriority.high, 3),
            (Task.priority == TaskPriority.medium, 2),
            (Task.priority == TaskPriority.low, 1),
        )

    else:
        sort_column = getattr(Task, sort_by.value)  
    
    sort_expression = (sort_column.asc() if sort_order == TaskSortOrder.asc else sort_column.desc())

    query = query.order_by(sort_expression, Task.id.desc())  # Secondary ordering by task ID in the event of a duplicate sort_by value


    # Pagination
        
    skip = (page - 1) * limit
    
    tasks = query.offset(skip).limit(limit).all()


    return {
        "data": tasks,
        "meta": {
            "total": total_tasks,
            "num_pages": num_pages,
            "page": page,
            "limit": limit
        }
    }


# =================
# GET SPECIFIC TASK
# =================


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    responses = {
        200: {"description": "OK - Successfully returned task"},
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from get_current_user
        403: {"description": "Forbidden - User account is inactive or the requested task does not belong to the logged-in user"},  # Stems from get_current_user, get_task_or_raise
        404: {"description": "Not Found - Task not found using the provided ID"},  # Stems from get_task_or_raise
        422: {"description": "Validation Error - Task ID is not an integer greater than 0"}
    }
)
@limiter.limit("60/minute")
def get_task_by_id(
    request: Request, 
    task_id: int = Path(gt=0, description="ID must be greater than 0"),    
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns a specific task by ID.

    Rate Limit:
    - 60 requests per minute

    1. Utilizes the imported get_current_user function to validate the provided token.
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive, raises a 403 error. 
    4. Attempts to locate the task in the database using the provided ID.
    5. If the provided ID is not an integer greater than 0, raises a 422 error.
    6. If the task cannot be found, raises a 404 error.
    7. If the task does not belong to the logged-in user, raises a 403 error.
    8. Otherwise, returns the requested task.    

    Standard Response: 
    - 200 - OK (successfully returned the task)
    
    Possible Errors:
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive or the requested task does not belong to the logged-in user)
    - 404 - Not Found (the task was not found using the provided ID)
    - 422 - Validation Error (the task ID is not an integer greater than 0)   
    """  
        
    return get_task_or_raise(task_id, db, current_user)
    

# ===========
# UPDATE TASK
# ===========


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    responses = {
        200: {"description": "OK - Successfully updated the task"},
        400: {"description": "Bad Request - Request is empty"},
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from get_current_user
        403: {"description": "Forbidden - User account is inactive or the requested task does not belong to the logged-in user"},  # Stems from get_current_user, get_task_or_raise
        404: {"description": "Not Found - Task not found using the provided ID"},  # Stems from get_task_or_raise
        422: {"description": "Validation Error - Check request body and/or Task ID is not an integer greater than 0"},
        500: {"description": "Internal Error - An error occurred while attempting to update the database"}
    }
)
@limiter.limit("30/minute")
def update_task(
    request: Request, 
    background_tasks: BackgroundTasks,
    task_data: TaskUpdate,    
    task_id: int = Path(gt=0, description="ID must be greater than 0"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates a specific task.  
    
    Rate Limit:
    - 30 requests per minute  
    
    The request body should contain:
    - **title**: (Optional) The task's new title (string, must be between 1-200 characters)
    - **description**: (Optional) The task's new description (string, must be between 1-2000 characters; can be set to null to clear the description)
    - **priority**: (Optional) The task's new priority level (one of "low", "medium", "high", "urgent")
    - **completed**: (Optional) The task's new completion status (boolean)

    1. Utilizes the imported get_current_user function to validate the provided token and return the current user.
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive, raises a 403 error.
    4. Attempts to locate the task in the database using the provided ID.
    5. If the provided ID is not an integer greater than 0, raises a 422 error.
    6. If the task cannot be found, raises a 404 error.
    7. If the task does not belong to the logged-in user, raises a 403 error.
    8. If the request is empty, raises a 400 error.    
    9. If other validation constraints are violated, raises a 422 error.    
    10. Otherwise, attempts to store the submitted updates in the database.
    11. If SUCCESSFUL, returns the updated task. (**Background task**: creates an activity log for this user/task.)
    12. If UNSUCCESSFUL, raises a 500 error and rolls back the database to its previous state.

    Returns:
    - The updated task

    Standard Response: 
    - 200 - OK (successfully updated the task)
    
    Possible Errors:
    - 400 - Bad Request (the request is empty)
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive or the requested task does not belong to the logged-in user)    
    - 404 - Not Found (the task was not found using the provided ID)
    - 422 - Validation Error (one or more of the validation requirements has been violated and/or the task ID is not an integer greater than 0)
    - 500 - Internal Error (an error occurred while attempting to update the task in the database)
    """    

    task = get_task_or_raise(task_id, db, current_user)
    
    update_data = {
        k: v
        for k, v in task_data.model_dump(exclude_unset=True).items()
        if v is not None or k == "description"
    }

    if not update_data:
        raise BadRequestException("No fields provided to update.")   
    
    try:
        for field, value in update_data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)
    
    except Exception:
        db.rollback()
        raise InternalError(f"Task {task_id} was not updated.")

    changes = ", ".join(update_data.keys())    
    background_tasks.add_task(create_activity_log, current_user.id, task.id, task.title, action="updated", changes=changes)

    return task


# ===========
# DELETE TASK
# ===========


@router.delete(
    "/{task_id}",
    responses = {
        200: {"description": "OK - Successfully deleted the task"},       
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from get_current_user
        403: {"description": "Forbidden - User account is inactive or the requested task does not belong to the logged-in user"},  # Stems from get_current_user, get_task_or_raise
        404: {"description": "Not Found - Task not found using the provided ID"},  # Stems from get_task_or_raise
        422: {"description": "Validation Error - Task ID is not an integer greater than 0"},
        500: {"description": "Internal Error - An error occurred while attempting to delete the task from the database"}
    }
)
@limiter.limit("10/minute")
def delete_task(
    request: Request,
    background_tasks: BackgroundTasks,
    task_id: int = Path(gt=0, description="ID must be greater than 0"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Deletes a specific task.
    
    Rate Limit:
    - 10 requests per minute

    1. Utilizes the imported get_current_user function to validate the provided token.
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive, raises a 403 error. 
    4. Attempts to locate the task in the database using the provided ID.
    5. If the provided ID is not an integer greater than 0, raises a 422 error.
    6. If the task cannot be found, raises a 404 error.
    7. If the task does not belong to the logged-in user, raises a 403 error.
    8. Otherwise, attempts to delete the task from the database.
    9. If SUCCESSFUL, returns a success message. (**Background task**: creates an activity log for this user/task.)
    10. If UNSUCCESSFUL, raises a 500 error and rolls back the database to its previous state.   

    Returns:
    - A success message
    
    Standard Response: 
    - 200 - OK (successfully deleted the task)
    
    Possible Errors:
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive or the requested task does not belong to the logged-in user)
    - 404 - Not Found (the task was not found using the provided ID)
    - 422 - Validation Error (the task ID is not an integer greater than 0)
    - 500 - Internal Error (an error occurred while attempting to delete the task from the database)
    """

    task = get_task_or_raise(task_id, db, current_user)
    task_title = task.title

    try:       
        db.query(ActivityLog).filter(ActivityLog.task_id == task.id).update({ActivityLog.task_id: None})  # For data integrity, sets the task ID on associated ActivityLog  entries to None (NULL) before deleting the task
        
        db.delete(task)
        db.commit()        
    
    except Exception:
        db.rollback()
        raise InternalError(f"Task {task_id} was not deleted.")

    background_tasks.add_task(create_activity_log, current_user.id, None, task_title, action="deleted")
    return {"message": f"Task {task_id} deleted successfully."}


# =================
# AI-READY ENDPOINT
# =================


@router.post(
    "/{task_id}/suggest",
    responses = {
        200: {"description": "OK - Successfully returned the sample AI suggestion"},       
        401: {"description": "Unauthorized - Invalid or expired token"},  # Stems from get_current_user
        403: {"description": "Forbidden - User account is inactive or the requested task does not belong to the logged-in user"},  # Stems from get_current_user, get_task_or_raise
        404: {"description": "Not Found - Task not found using the provided ID"},  # Stems from get_task_or_raise
        422: {"description": "Validation Error - Task ID is not an integer greater than 0"}        
    }
)
@limiter.limit("5/minute")
def suggest_task_action(
    request: Request,
    task_id: int = Path(gt=0, description="ID must be greater than 0"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns a placeholder AI-generated suggestion for a task.

     Rate Limit:
    - 5 requests per minute

    1. Utilizes the imported get_current_user function to validate the provided token.
    2. If the token cannot be validated or has expired, raises a 401 error.
    3. If the user account is inactive, raises a 403 error. 
    4. Attempts to locate the task in the database using the provided ID.
    5. If the provided ID is not an integer greater than 0, raises a 422 error.
    6. If the task cannot be found, raises a 404 error.
    7. If the task does not belong to the logged-in user, raises a 403 error.
    8. Otherwise, returns the sample AI suggestion. 
  
    Standard Response: 
    - 200 - OK (successfully returned the sample AI suggestion)
    
    Possible Errors:
    - 401 - Unauthorized (the provided token is invalid or expired)
    - 403 - Forbidden (the user account is inactive or the requested task does not belong to the logged-in user)
    - 404 - Not Found (the task was not found using the provided ID)
    - 422 - Validation Error (the task ID is not an integer greater than 0)    
    """

    task = get_task_or_raise(task_id, db, current_user)
    
    return {
        "task_id": task.id,
        "suggestion": "Sample AI task suggestion (available in a future version of this app)"
    }