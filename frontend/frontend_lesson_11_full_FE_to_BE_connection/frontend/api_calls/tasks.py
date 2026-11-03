from frontend.api_calls.client import api_request


def get_all_tasks(headers: dict, sort_by: str = "priority", sort_order: str = "desc"):
    """Get all tasks for the logged-in user."""    
    
    return api_request(
        "GET",
        "/tasks/",
        headers=headers,
        params={
            "sort_by": sort_by,
            "sort_order": sort_order
        }
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
        f"/tasks",
        headers=headers,
        json=task_details       
    )