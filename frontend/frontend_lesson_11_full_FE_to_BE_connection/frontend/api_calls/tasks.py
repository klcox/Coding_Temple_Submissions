from frontend.api_calls.client import api_request


def get_all_tasks(
        headers: dict, 
        sort_by: str = "priority", 
        sort_order: str = "desc",
        page: int = 1,
        limit: int = 10
):
    """Get all tasks for the logged-in user. Includes sorting preferences and pagination."""    
    
    return api_request(
        "GET",
        "/tasks/",
        headers=headers,
        params={
            "sort_by": sort_by,
            "sort_order": sort_order,
            "page": page,
            "limit": limit
        }
    )


def get_task_metrics(headers: dict):
    """Get task metrics for the logged-in user's tasks."""

    return api_request(
        "GET",
        "/tasks/metrics",
        headers=headers        
    )


def update_task_status(headers: dict, task_id: int, status: bool):
    """Update the 'completed' status for a specific task."""    

    return api_request(
        "PATCH",
        f"/tasks/{task_id}",
        headers=headers,
        json={
            "completed": status
        }
    )


def update_task_details(headers: dict, task_id: int, task_updates: dict):
    """Update the details for a specific task (title, description, and/or priority)."""

    return api_request(
        "PATCH",
        f"/tasks/{task_id}",
        headers=headers,
        json=task_updates
    )


def delete_task(headers: dict, task_id: int):
    """Delete a specific task."""    

    return api_request(
        "DELETE",
        f"/tasks/{task_id}",
        headers=headers        
    )


def add_new_task(headers: dict, task_details: dict):
    """Add a new task for the logged-in user."""    

    return api_request(
        "POST",
        f"/tasks/",
        headers=headers,
        json=task_details       
    )