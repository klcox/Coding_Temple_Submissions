from fastapi import APIRouter, Request, Depends, Query, Path, BackgroundTasks
from app.utils.limiter import limiter
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.utils.security import get_current_user
from app.models.user import User
from app.models.task import Task
from app.models.activity import ActivityLog
from typing import Optional
from app.enums import TaskPriority, TaskSort, TaskSortOrder
from app.utils.exceptions import InternalError, NotFoundException, ForbiddenException, BadRequestException


router = APIRouter(
    prefix = "/tasks",
    tags = ["Tasks"]
)


# ================
# HELPER FUNCTIONS
# ================

def create_activity_log(user_id, task_id, task_title, action):
        
    new_log = ActivityLog(
        user_id = user_id,
        task_id = task_id,
        task_title = task_title,
        action = action
    )

    db = SessionLocal()

    try:
        db.add(new_log)
        db.commit()          

    except Exception as err_msg:  
        db.rollback()
        raise InternalError(f"Task was not logged. Error: {err_msg}")

    finally: db.close()


def get_task_or_4XX(task_id: int, db: Session, current_user: User):

    task = db.query(Task).filter(Task.id == task_id).first()
        
    if not task:
        raise NotFoundException("Task", f"ID {task_id}")

    if task.user_id != current_user.id:
        raise ForbiddenException("You do not have permission to access this task.")

    return task


# ==============
# TASK ENDPOINTS
# ==============


@router.post("/", response_model=TaskResponse, status_code=201)
@limiter.limit("30/minute")
def create_task(
    request: Request, 
    task: TaskCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):

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


@router.get("/", response_model=list[TaskResponse])
@limiter.limit("60/minute")
def get_all_tasks(
    request: Request,
    completed: Optional[bool] = Query(default=None, description="Filter by completion status"),
    priority: Optional[TaskPriority] = Query(default=None, description="Filter by priority"),
    search: Optional[str] = Query(default=None, min_length=1, max_length=200, description="Search task title"),
    sort_by: TaskSort = TaskSort.priority,
    sort_order: TaskSortOrder = TaskSortOrder.desc,
    skip: int = Query(default=0, ge=0, description="Number of tasks to skip for pagination"),
    limit: int = Query(default=10, ge=1, le=20, description="Max number of results for pagination"),
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):

    query = db.query(Task).filter(Task.user_id == current_user.id)


    # Filtering

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    if search is not None:
        query = query.filter(Task.title.ilike(f"%{search}%"))


    # Sorting
    
    query = query.order_by(getattr(Task, sort_by.value).asc() if sort_order == TaskSortOrder.asc else getattr(Task, sort_by.value).desc())


    # Pagination

    query = query.offset(skip).limit(limit)


    tasks = query.all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
@limiter.limit("60/minute")
def get_task_by_id(
    request: Request, 
    task_id: int = Path(gt=0, description="ID must be greater than 0"),
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return get_task_or_4XX(task_id, db, current_user)
    

@router.patch("/{task_id}", response_model=TaskResponse)
@limiter.limit("30/minute")
def update_task(
    request: Request, 
    task_data: TaskUpdate,
    background_tasks: BackgroundTasks,
    task_id: int = Path(gt=0, description="ID must be greater than 0"),    
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):        

    task = get_task_or_4XX(task_id, db, current_user)
    
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

    background_tasks.add_task(create_activity_log, current_user.id, task.id, task.title, action="updated")
    return task


@router.delete("/{task_id}")
@limiter.limit("10/minute")
def delete_task(
    request: Request,
    background_tasks: BackgroundTasks,
    task_id: int = Path(gt=0, description="ID must be greater than 0"),    
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):

    task = get_task_or_4XX(task_id, db, current_user)
    task_title = task.title

    try:       
        db.query(ActivityLog).filter(ActivityLog.task_id == task.id).update({ActivityLog.task_id: None})  # For data integrity, sets the task ID on associated ActivityLog  entries to None (NULL) before deleting
        
        db.delete(task)
        db.commit()        
    
    except Exception:
        db.rollback()
        raise InternalError(f"Task {task_id} was not deleted.")

    background_tasks.add_task(create_activity_log, current_user.id, None, task_title, action="deleted")
    return {"message": f"Task {task_id} deleted successfully."}


@router.post("/{task_id}/suggest")
@limiter.limit("5/minute")
def suggest_task_action(
    request: Request,
    task_id: int = Path(gt=0, description="ID must be greater than 0"),    
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):

    task = get_task_or_4XX(task_id, db, current_user)
    
    return {
        "task_id": task.id,
        "suggestion": "Sample AI task suggestion (available in a future version of this app)"
    }