def test_create_task(client):
    """Test: POST /tasks creates a task and returns 201."""
   
    response = client.post("/tasks", json={
        "title": "Buy groceries",
        "completed": False
    })

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Buy groceries"
    assert "id" in data


def test_list_tasks(client):
    """Test: GET /tasks returns 200 and a list."""

    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_by_id(client, sample_task):
    """Test: GET /tasks/{id} returns the created task."""

    response = client.get(f"/tasks/{sample_task['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Test Title"


def test_get_nonexistent_task_returns_404(client):
    """Test: GET /tasks/9999 returns 404."""

    response = client.get("/tasks/9999")

    assert response.status_code == 404


def test_patch_task(client, sample_task):
    """Test: PATCH /tasks/{id} updates only the specified fields."""

    response = client.patch(f"/tasks/{sample_task['id']}", json={
        "completed": True
    })

    assert response.status_code == 200
    assert response.json()["completed"] is True  # Reflects updated data
    assert response.json()["title"] == "Test Title"  # Should remain unchanged


def test_delete_task(client, sample_task):
    """Test: DELETE /tasks/{id} removes the task."""

    response = client.delete(f"/tasks/{sample_task['id']}")
    assert response.status_code == 200

    response = client.get(f"/tasks/{sample_task['id']}")  # Verify the resource has been deleted
    assert response.status_code == 404


def test_create_task_invalid_data_returns_422(client):
    """Test: POST /tasks with an empty title returns 422."""

    response = client.post("/tasks", json={  # Empty string violates min_length=1
        "title": ""
    })

    assert response.status_code == 422


def test_duplicate_task_title_returns_409(client):
    """Test: Creating two tasks with the same title returns 409."""

    response = client.post("/tasks", json={
        "title": "Unique Task"
    })
    assert response.status_code == 201

    response = client.post("/tasks", json={  # Repeat request (duplicate title)
        "title": "Unique Task"
    })
    assert response.status_code == 409