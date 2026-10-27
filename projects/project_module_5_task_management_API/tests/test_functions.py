from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings
from app.models.user import User
from app.models.activity import ActivityLog


def test_health_check(client):
    """Test: Health check - root returns 200."""

    response = client.get("/")

    assert response.status_code == 200  # OK - Success
    assert response.json()["docs"] == "/docs"


# ===============
# AUTH - REGISTER
# ===============


def test_registration_success(client):
    """Test: POST /auth/register returns 201 and the user object without the password when successful."""

    response = client.post("/auth/register", json={
        "username": "new_username",
        "email": "new_user@test.com",
        "password": "password123"
    })

    assert response.status_code == 201  # Created

    data = response.json()
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data


def test_register_duplicate_username(client, sample_user):
    """Test: POST /auth/register raises a 409 error when username is not unique."""

    response = client.post("/auth/register", json={
        "username": "test_username",
        "email": "user_email@test.com",
        "password": "password123"
    })

    assert response.status_code == 409  # Conflict (DuplicateException)
    print(response.json())


def test_register_duplicate_email(client, sample_user):
    """Test: POST /auth/register raises a 409 error when email is not unique."""

    response = client.post("/auth/register", json={
        "username": "sample_username",
        "email": "sample_email@test.com",
        "password": "password456"
    })

    assert response.status_code == 409  # Conflict (DuplicateException)
    print(response.json())


def test_email_validation(client):
    """Test: POST /auth/register raises a 422 validation error when email is missing '@'."""

    response = client.post("/auth/register", json={
        "username": "sample_username",
        "email": "sample_emailtest.com",
        "password": "password789"
    })

    assert response.status_code == 422  # Validation Error
    print(response.json())


# ============
# AUTH - LOGIN
# ============


def test_login_success(client, sample_user):
    """Test: POST /auth/login returns 200 and a JWT upon validating a user's username and password."""

    response = client.post("/auth/login", data={
        "username": sample_user["username"],
        "password": "test_password"
    })

    assert response.status_code == 200  # OK - Success
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_incorrect_username(client, sample_user):
    """Test: POST /auth/login raises a 401 error when the username is incorrect."""

    response = client.post("/auth/login", data={
        "username": "wrong_username",
        "password": "test_password"
    })

    assert response.status_code == 401  # Unauthorized
    print(response.json())


def test_login_incorrect_password(client, sample_user):
    """Test: POST /auth/login raises a 401 error when the password is incorrect."""

    response = client.post("/auth/login", data={
        "username": sample_user["username"],
        "password": "wrong_password"
    })

    assert response.status_code == 401  # Unauthorized
    print(response.json())


def test_login_inactive_user(client, deactivated_user):
    """Test: POST /auth/login raises a 403 error when the user is deactivated (inactive)."""

    response = client.post("/auth/login", data={
        "username": deactivated_user["username"],
        "password": "test_password"            
    })

    assert response.status_code == 403  # Forbidden
    print(response.json())


# =================
# JWT AUTHORIZATION
# =================


def test_no_auth_headers(client):
    """Test: get_current_user raises a 401 error when no authorization headers are provided."""

    response = client.get("/users/me")
    
    assert response.status_code == 401  # Unauthorized
    print(response.json())


def test_invalid_token(client, sample_auth_headers):
    """Test: get_current_user raises a 401 error when an invalid token is provided."""

    response = client.get("/users/me", headers= {
        "Authorization": "Bearer fake_token"
    })

    assert response.status_code == 401  # Unauthorized
    print(response.json())


def test_expired_token(client):
    """Test: get_current_user raises a 401 error when a token is expired."""

    token = jwt.encode(
        {
            "sub": "test_username",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=5)
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    response = client.get("/users/me",headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 401  # Unauthorized
    print(response.json())


def test_valid_token_inactive_user(client, deactivated_user, sample_auth_headers):
    """Test: get_current_user raises a 403 error when a deactivated user with a valid token attempts to perform an action."""

    response = client.get("/users/me", headers=sample_auth_headers)

    assert response.status_code == 403  # Forbidden
    print(response.json())


def test_admin_only_activity_logs(client, sample_auth_headers):
    """Test: verify_admin_status raises a 403 error for an admin-only endpoint when the user is not an admin."""

    response = client.get("/users/activity", headers=sample_auth_headers)

    assert response.status_code == 403  # Forbidden
    print(response.json())


# ==============
# USER ENDPOINTS
# ==============


def test_get_user_profile_success(client, sample_auth_headers):
    """Test: GET /users/me returns 200 and the user profile (object) without the password when successful."""

    response = client.get("/users/me", headers=sample_auth_headers)

    assert response.status_code == 200  # OK - Success

    data = response.json()
    assert "id" in data
    assert "password" not in data


def test_user_patch_success(client, sample_auth_headers, sample_user):
    """Test: PATCH /users/me returns 200 and the updated user object (still without password) when successful."""

    response = client.patch(
        "/users/me", 
        headers=sample_auth_headers,
        json={
            "password": "new_password"
    })

    assert response.status_code == 200  # OK - Success

    data = response.json()
    assert data["email"] == "sample_email@test.com"  # Unchanged
    assert "password" not in data


    response = client.post("/auth/login", data={  # Verify that the user can log-in using the new password
        "username": sample_user["username"],
        "password": "new_password"
    })

    assert response.status_code == 200  # OK - Success


def test_user_patch_bad_request(client, sample_auth_headers):
    """Test: PATCH /users/me raises a 400 error when the request does not include any fields to update."""

    response = client.patch(
        "/users/me", 
        headers=sample_auth_headers,
        json={}
    )

    assert response.status_code == 400  # Bad Request
    print(response.json())


def test_user_patch_duplicate_email(client, sample_auth_headers):
    """Test: PATCH /users/me raises a 409 error when a user attempts to update their email but the email already exists for another user in the database."""

    response = client.post("/auth/register", json={  # Create a new (second) user
        "username": "new_username",
        "email": "new_user@test.com",
        "password": "password123"
    })

    assert response.status_code == 201  # Created
    
    
    response = client.patch(  # Try to update the first user's email using the existing email from the second user
        "/users/me", 
        headers=sample_auth_headers,
        json={
            "email": "new_user@test.com"
    })

    assert response.status_code == 409  # Conflict (DuplicateException)
    print(response.json())


def test_deactivate_user_success(client, sample_auth_headers, sample_user, db_session):
    """Test: DELETE /users/me returns 200, preserves the user in the database, and updates a user's 'is_active' status from True to False when successful."""

    response = client.delete("/users/me", headers=sample_auth_headers)

    assert response.status_code == 200  # OK - Success
    print(response.json())  # Should reflect success message


    user = db_session.query(User).filter(User.id == sample_user["id"]).first()  # Verify that the user still exists but is now deactivated

    assert user is not None
    assert user.is_active is False


# ==============
# TASK ENDPOINTS
# ==============


def test_create_task_success(client, sample_auth_headers):
    """Test: POST /tasks returns 201 and the task object when successful."""
   
    response = client.post(
        "/tasks",
        headers=sample_auth_headers,
        json={
            "title": "Clean the kitchen",
            "description": "Dishes, Disinfect counters, Mop",
            "priority": "high"
    })

    assert response.status_code == 201  # Created

    data = response.json()
    assert data["title"] == "Clean the kitchen"
    assert data["priority"] == "high"  # As opposed to default of "medium"
    assert "id" in data
 
    
def test_create_task_validation_error(client, sample_auth_headers):
    """Test: POST /tasks raises a 422 error when request fields violate validation constraints."""

    response = client.post(
        "/tasks",
        headers=sample_auth_headers,
        json={
            "title": ""
    })

    assert response.status_code == 422  # Validation Error (Title cannot be an empty string.)
    print(response.json())


def test_get_all_tasks_success(client, sample_auth_headers, sample_task):
    """Test: GET /tasks returns 200 and all of a user's tasks when successful."""

    response = client.get("/tasks", headers=sample_auth_headers)

    assert response.status_code == 200  # OK - Success
    assert response.json()["data"][0]["title"] == "Test Title"


def test_get_specific_task_success(client, sample_auth_headers, sample_task):
    """Test: GET /task/{task_id} returns 200 and the user's requested task when successful."""

    response = client.get(f"/tasks/{sample_task['id']}", headers=sample_auth_headers)

    assert response.status_code == 200  # OK - Success
    assert response.json()["title"] == "Test Title"


def test_task_not_found(client, sample_auth_headers, sample_task):
    """Test: get_task_or_404 raises a 404 error when the requested task cannot be found."""

    response = client.get("/tasks/999", headers=sample_auth_headers)

    assert response.status_code == 404  # Not Found
    print(response.json())


def test_task_belongs_to_other_user(client, sample_auth_headers, sample_task, sample_admin_task):
    """Test: get_task_or_404 raises a 404 error when the requested task does not belong to the logged-in user."""

    response = client.get(
        f"/tasks/{sample_admin_task['id']}", 
        headers=sample_auth_headers
    )

    assert response.status_code == 404  # Not Found
    print(response.json())


def test_update_task_success(client, sample_auth_headers, sample_task):
    """Test: PATCH /task/{task_id} returns 200 and the updated task object when successful."""

    response = client.patch(
        f"/tasks/{sample_task['id']}", 
        headers=sample_auth_headers,
        json={
            "completed": True
    })

    assert response.status_code == 200  # OK - Success

    assert response.json()["completed"] is True  
    assert response.json()["title"] == "Test Title"  # Unchanged


def test_delete_task_success(client, sample_auth_headers, sample_task):
    """Test: DELETE /task/{task_id} returns 200 and a success message when successful."""  
        
    response = client.delete(f"/tasks/{sample_task['id']}", headers=sample_auth_headers)

    assert response.status_code == 200  # OK - Success
    print(response.json())  # Should reflect success message


    response = client.get(f"/tasks/{sample_task['id']}", headers=sample_auth_headers)  # Verify that the task is deleted

    assert response.status_code == 404  # Not Found
    print(response.json())


def test_ai_ready_endpoint_success(client, sample_auth_headers, sample_task):
    """Test: GET /tasks/{task_id}/suggest returns 200 and the placeholder AI suggestion when successful."""

    response = client.get(f"/tasks/{sample_task['id']}/suggest", headers=sample_auth_headers)

    assert response.status_code == 200  # OK - Success
    print(response.json())  # Should reflect placeholder suggestion response


# ================
# BACKGROUND TASKS
# ================


def test_background_task_created(client, sample_task, db_session):
    """Test: POST /tasks - when a new task is created successfully, the background task also runs successfully and creates an activity log ("created")."""

    log = db_session.query(ActivityLog).filter(ActivityLog.task_id == sample_task["id"], ActivityLog.action == "created").first()

    assert log is not None
    assert log.task_title == "Test Title"    


def test_background_task_updated(client, sample_auth_headers, sample_task, db_session):
    """Test: PATCH /task/{task_id} - when a new task is updated successfully, the background task also runs successfully and creates an activity log ("updated")."""

    response = client.patch(  # Update task
        f"/tasks/{sample_task['id']}", 
        headers=sample_auth_headers,
        json={
            "completed": True
    })

    assert response.status_code == 200  # OK - Success

    
    log = db_session.query(ActivityLog).filter(ActivityLog.task_id == sample_task["id"], ActivityLog.action == "updated").first()

    assert log is not None
    assert log.task_title == "Test Title"     


def test_background_task_deleted(client, sample_auth_headers, sample_task, db_session):
    """Test: DELETE /task/{task_id} - when a new task is deleted successfully, the background task also runs successfully and creates an activity log ("deleted")."""

    response = client.delete(f"/tasks/{sample_task['id']}", headers=sample_auth_headers)  # Delete task
    
    assert response.status_code == 200  # OK - Success

    
    log = db_session.query(ActivityLog).filter(ActivityLog.task_title == sample_task["title"], ActivityLog.action == "deleted").first()
    
    assert log is not None
    assert log.task_id is None     


# =========================================
# FILTERING, QUERY PARAMETERS, & PAGINATION
# =========================================


def test_task_filtering(client, sample_auth_headers, sample_task):
    """Test: GET /tasks with a filtering query parameter returns 200 when successful and returns the correct schema when there are no results to display."""

    response = client.get("/tasks?completed=true", headers=sample_auth_headers)

    assert response.status_code == 200  # OK - Success
    assert response.json()["data"] == []  # sample_task defaults to "completed": False, meaning no results would display under this filter
    assert response.json()["meta"]["total"] == 0


def test_activity_log_pagination(client, sample_admin_auth_headers, sample_task, sample_admin_task):
    """Test: GET /users/activity with page and limit parameters returns 200 when successful and the correct page/results."""

    response = client.get("/users/activity", headers=sample_admin_auth_headers, params={
        "page": 2, "limit": 1
    })

    assert response.status_code == 200  # OK - Success
    assert "id" in response.json()["data"][0]
    assert response.json()["meta"]["total"] == 2
    assert response.json()["meta"]["page"] == 2
    assert response.json()["meta"]["limit"] == 1