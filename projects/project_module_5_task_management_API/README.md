# Task Management API

**Version**: v1

**Authentication**: JWT Bearer Token

This project pertains to a task management app, where users register an account and create/manage their own tasks.

## Core Technologies
- FastAPI
- Pydantic
- SQLAlchemy
- Pytest
- SlowAPI
- Uvicorn
- Swagger UI

## Features
- User registration, JWT authentication, and Admin verification
- CORS Middleware configuration
- Rate limiting
- Full CRUD for tasks, including filtering, sorting, and pagination
- Background task processing related to user activity logs
- Validation and error handling
- An AI-ready endpoint
- Pytest testing
- Interactive documentation

## Resources, Relationships, & Database Design
| Relationship | Type | Description |
|---|---|---|
| User, Task | One-to-many | One user can have many tasks, but each task pertains to only one user. |
| User/Task, ActivityLog | One-to-many | One user and/or one task can have many associated ActivityLogs, but each ActivityLog pertains to only one user and one task. |

### ERD Visualization:
(Attributes are required/non-nullable unless otherwise specified)

    [User]         ----->         [Task]
    PK id                         PK id
    username (unique)		  FK user_id
    email (unique)                title
    hashed_password               description (optional)
    is_active                     priority (enum)
    is_admin                      completed
    created_at                    created_at
                                  updated_at
                                    
    |                                |
    |                                |
    |                                |
    |                                |
    |                                |
    |                                |
    |                                |
    ->        [Activity Log]        <-        
               PK id
               FK user_id
               FK task_id (can be None [NULL] once a task is deleted)
               task_title
               action (enum)
               changes (intended for use with PATCH; otherwise can be None [NULL])
               timestamp

## Project Structure
```text
app/
├── __init__.py          — Designates the directory as a Python package
├── config.py            — Application settings and .env configuration
├── database.py          — SQLAlchemy engine and session set-up
├── main.py              — FastAPI app definition (+ CORS Middleware, Rate Limiting, Exception Handlers, Routers, Root)
├── seed_data.py         — Creates a sample admin user for testing and demo purposes
│
├── models/
│     ├── __init__.py    — Designates the directory as a Python package
│     ├── activity.py    — ActivityLog ORM model
│     ├── task.py        — Task ORM model
│     └── user.py        — User ORM model
│
├── routers/
│      ├── __init__.py   — Designates the directory as a Python package
│      ├── auth.py       — Registration and login endpoints
│      ├── tasks.py      — Task CRUD and AI-ready endpoint
│      └── users.py      — User CRUD and admin-only activity log endpoint
│
├── schemas/
│     ├── __init__.py    — Designates the directory as a Python package
│     ├── activity.py    — ActivityLog create, response, and pagination schemas
│     ├── task.py        — Task create, update, response, and pagination schemas
│     └── user.py        — User create, update, response, and token schemas
│
├── utils/
│     ├── __init__.py    — Designates the directory as a Python package
│     ├── enums.py       — Enumerations (TaskPriority, TaskSort, TaskSortOrder, ActivityLogAction)
│     ├── exceptions.py  — Custom error handling
│     ├── limiter.py     — Rate-limiting configuration 
│     └── security.py    — JWT authentication and admin verification
│
tests/
├── __init__.py          — Designates the directory as a Python package
├── conftest.py          — Test database configuration and Pytest fixtures
├── test_functions.py    — Test cases
│
.env.example.env          — Placeholder .env file
.gitignore                — Files excluded from Git
pytest.ini                — Test discovery and app import path
README.md                 — Project documentation (This file)
requirements.txt          — Packages and dependencies
```

## Endpoints & Authentication
***Note: A user can only access their own profile and their own tasks***

### Auth

| HTTP Method | URI | Description | Auth Required? | Who Can Access? |
|---|---|---|---|---|
| POST | /auth/register | Creates a new user in the database | No | Public |
| POST | /auth/login | Validates credentials and returns a JWT if verified | No | Public |

### Users

| HTTP Method | URI | Description | Auth Required? | Who Can Access? |
|---|---|---|---|---|
| GET | /users/me | Returns the logged-in user's profile | Yes | Logged-in user |
| PATCH | /users/me | Updates a user's profile (email and/or password) | Yes | Logged-in user |
| DELETE | /users/me | Deactivates a user account | Yes | Logged-in user |
| GET | /users/activity | Returns user activity logs | Yes | Admin only |
| GET | /users/activity?action=created&page=2 | Returns filtered user activity logs | Yes | Admin only |

#### Includes options for filtering by:
- user_id (specific user)
- action (created, updated, deleted)
- start_date and/or end_date (date range)
- search (task title content)

#### Includes options for pagination:
- page (on which page to begin the results)
- limit (max number of results to display per page)

### Tasks

| HTTP Method | URI | Description | Auth Required? | Who Can Access? |
|---|---|---|---|---|
| POST | /tasks | Creates a new task | Yes | Logged-in user |
| GET | /tasks | Returns a user's tasks | Yes | Logged-in user |
| GET | /tasks?completed=false&page=2 | Returns a user's filtered tasks | Yes | Logged-in user |
| GET | /tasks/{task_id} | Returns a specific task by ID | Yes | Logged-in user |
| PATCH | /tasks/{task_id} | Updates a specific task | Yes | Logged-in user |
| DELETE | /tasks/{task_id} | Deletes a specific task | Yes | Logged-in user |
| GET | /tasks/{task_id}/suggest | Returns a placeholder AI-suggestion for a task | Yes | Logged-in user |

#### Includes options for filtering by:
- completed (true or false)
- priority (low, medium, high, urgent)
- search (task title content)

#### Includes options for sorting:
- sort_by (created_at, title, completed, priority)
- sort_order (asc [ascending] or desc [descending])

#### Includes options for pagination:
- page (on which page to begin the results)
- limit (max number of results to display per page)

## Sample Response Schemas

### POST /auth/login (Response: 200, OK)
``` json

{                
	"access_token": "SAMPLE_TOKEN",
	"token_type": "bearer"
}
```

### GET /users/me (Response: 200, OK)
***Note: password, is_active, and is_admin are excluded here for security purposes***
``` json
{                
	"id": 1,
	"username": "username123",
	"email": "email@test.com",                
	"created_at": "2026-10-12T10:30:00"
}
```

### GET /tasks (Response: 200, OK)
``` json
{                
	"data": [
		{
			"title": "Buy Groceries",
                        "description": "Apples, bananas, eggs, bread",
                        "priority": "medium",
                        "completed": False,
                        "id": 1,
                        "user_id": 1,
                        "created_at": "2026-10-13T12:00:00",
                        "updated_at": "2026-10-13T12:00:00" 
		},
		{
                        "title": "Finish Homework",                        
                        "priority": "high",
                        "completed": False,
                        "id": 2,
                        "user_id": 1,
                        "created_at": "2026-10-13T12:30:00",
                        "updated_at": "2026-10-13T12:30:00" 
		}
	],
	"meta": {
			"total": 2,
			"num_pages": 1,
			"page": 1,
			"limit": 10
                }              
}
```

### DELETE /tasks/1 (Response: 200, OK)
``` json
{
	"message": "Task 1 deleted successfully."
}
```

## Rate Limits
| HTTP Method | URI (Prefix) | Number of Requests Per Minute |
|---|---|---|
| POST | /auth | 5 |
| POST | /tasks | 30 |
| GET | /users, /tasks | 60 |
| GET | /tasks/{task_id}/suggest | 5 |
| PATCH | /users, /tasks | 30 |
| DELETE | /users, /tasks | 10 |

## Possible Responses & Error Codes
| Status Code | Description | Occurs When |
|---|---|---|
| 200 | OK - Successful | A resource or a paginated list of resources was successfully returned; a resource was successfully updated or deleted; log-in successfully validated the user and returned a token |
| 201 | Created | User registration or creation of a new task is successful | 
| 400 | Bad Request | A PATCH request is empty or missing required fields; a business rule is violated (e.g. the requested page exceeds the number of pages returned) |
| 401 | Unauthorized | Username/password is incorrect for login; a token is invalid or expired |
| 403 | Forbidden | A user is not allowed to perform an action as their account is deactivated; a non-admin user attempts to access an admin-only endpoint |
| 404 | Not Found | A resource cannot be found; a user attempts to access a task that does not belong to them *(404 instead of 403 for security purposes)* | 
| 409 | Conflict | A uniqueness constraint is violated for username or email |
| 422 | Validation Error | One or more of the validation requirements has been violated (e.g. a username longer than 50 characters or an empty task title) |
| 429 | Too Many Requests | A rate limit was exceeded within the designated timeframe (e.g. more then X requests per minute) |
| 500 | Internal Server Error | A database action such as POST, PATCH, or DELETE could not be performed due to a server/database error; unexpected exceptions |

## Special Note
`seed_data.py` is intended to be run with a **fresh** database so as to initialize the database with a sample admin user for testing. Running this file multiple times on an existing database may result in duplicate records or constraint errors. If the latter occurs, delete the database file (e.g. `task_management.db`) and the `__pycache__` folder; then try running `seed_data.py` again.

## Setup
1. Clone this repo
2. Create a virtual environment (e.g. for Windows/Git Bash: `python -m venv venv`)
3. Activate the virtual environment (e.g. for Windows/Git Bash: `source venv/Scripts/activate`)
4. Install dependencies (e.g. for Windows/Git Bash: `pip install -r requirements.txt`)
5. Copy `.env.example` to `.env` AND replace the Secret Key and Admin Password with values of your own choosing
6. THEN:

### To Interact with the Documentation
- Initialize the database and add the seed data: `python -m app.seed_data`
- Run the main program: `python -m uvicorn app.main:app --reload`
- In a browser, visit `http://127.0.0.1:8000/docs`
- Register at: `/auth/register`
- Enter your username and password at `/auth/login` **(Note the access token received in the response.)**
- Click the lock icon at the far-right of the endpoint you would like to test (or the 'Authorize' button at the top of the page)
- Paste the access token into the dialog box and click 'Authorize'
- Close the dialog box
- Click 'Try it out' and 'Execute' on the endpoints to test and view the responses

#### To Test the Admin User
- No need to register as the admin user is seeded in the initial steps above.
- Simply log-in at `/auth/login` using the admin username in `seed_data.py` and the admin password set-up in `.env`.
- Then, continue the steps above to test the endpoints.

### To Run Pytest Tests
- Run `python -m pytest tests/ -v` (or `python -m pytest tests/ -v -s` to see the full JSON responses where included)
