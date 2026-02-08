import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from datetime import datetime, timedelta
import json

from src.main import app
from src.database.database import engine, get_session
from src.models.models import User, Task
from src.auth.auth import create_access_token


@pytest.fixture(scope="module")
def client():
    """Create a test client for the API"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def setup_test_user_and_token():
    """Setup a test user and return their token"""
    with Session(engine) as session:
        # Clean up any existing test user
        existing_users = session.exec(select(User).where(User.email == "tasktest@example.com")).all()
        for user in existing_users:
            session.delete(user)
        session.commit()

        # Create a test user
        user = User(
            email="tasktest@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # "testpassword" hashed
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create a JWT token for the user
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        token = create_access_token(token_data)

        yield user, token

        # Cleanup: delete the test user
        session.delete(user)
        session.commit()


def test_create_task_success(client, setup_test_user_and_token):
    """Test creating a new task successfully"""
    user, token = setup_test_user_and_token

    response = client.post(
        f"/api/{user.id}/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "medium",
            "tags": '["testing", "important"]',
            "due_date": (datetime.now() + timedelta(days=1)).isoformat()
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["user_id"] == user.id
    assert data["completed"] is False
    assert data["priority"] == "medium"
    assert data["tags"] == ["testing", "important"]


def test_create_task_minimal_fields(client, setup_test_user_and_token):
    """Test creating a task with minimal required fields"""
    user, token = setup_test_user_and_token

    response = client.post(
        f"/api/{user.id}/tasks",
        json={"title": "Minimal Task"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["completed"] is False
    assert data["priority"] == "medium"  # Default value


def test_get_all_tasks(client, setup_test_user_and_token):
    """Test retrieving all tasks for a user"""
    user, token = setup_test_user_and_token

    # Create a test task first
    create_response = client.post(
        f"/api/{user.id}/tasks",
        json={"title": "Get Tasks Test"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Get all tasks
    response = client.get(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["tasks"]) >= 1

    # Find our test task in the response
    task_found = False
    for task in data["data"]["tasks"]:
        if task["id"] == task_id and task["title"] == "Get Tasks Test":
            task_found = True
            break
    assert task_found is True


def test_get_single_task(client, setup_test_user_and_token):
    """Test retrieving a single task"""
    user, token = setup_test_user_and_token

    # Create a test task first
    create_response = client.post(
        f"/api/{user.id}/tasks",
        json={"title": "Single Task Test"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Get the single task
    response = client.get(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Single Task Test"


def test_update_task(client, setup_test_user_and_token):
    """Test updating an existing task"""
    user, token = setup_test_user_and_token

    # Create a test task first
    create_response = client.post(
        f"/api/{user.id}/tasks",
        json={"title": "Original Title", "description": "Original Description"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Update the task
    response = client.put(
        f"/api/{user.id}/tasks/{task_id}",
        json={
            "title": "Updated Title",
            "description": "Updated Description",
            "priority": "high"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["priority"] == "high"


def test_toggle_task_completion(client, setup_test_user_and_token):
    """Test toggling task completion status"""
    user, token = setup_test_user_and_token

    # Create a test task first
    create_response = client.post(
        f"/api/{user.id}/tasks",
        json={"title": "Completion Test Task"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Verify initial state (should be incomplete)
    get_response = client.get(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.json()["completed"] is False

    # Toggle completion to true
    response = client.patch(
        f"/api/{user.id}/tasks/{task_id}/complete",
        json={"completed": True},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["completed"] is True

    # Toggle completion back to false
    response = client.patch(
        f"/api/{user.id}/tasks/{task_id}/complete",
        json={"completed": False},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["completed"] is False


def test_delete_task(client, setup_test_user_and_token):
    """Test deleting a task"""
    user, token = setup_test_user_and_token

    # Create a test task first
    create_response = client.post(
        f"/api/{user.id}/tasks",
        json={"title": "Delete Test Task"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Verify task exists
    get_response = client.get(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200

    # Delete the task
    response = client.delete(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # Verify task no longer exists
    get_response = client.get(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404


def test_user_isolation(client, setup_test_user_and_token):
    """Test that users can only access their own tasks"""
    user, token = setup_test_user_and_token

    # Create a test task for the user
    create_response = client.post(
        f"/api/{user.id}/tasks",
        json={"title": "User Isolation Test"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Create another user
    with Session(engine) as session:
        other_user = User(
            email="otheruser@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # "testpassword" hashed
        )
        session.add(other_user)
        session.commit()
        session.refresh(other_user)

        # Create token for other user
        other_token_data = {
            "user_id": other_user.id,
            "email": other_user.email,
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        other_token = create_access_token(other_token_data)

    # Try to access the original user's task with other user's token
    response = client.get(
        f"/api/{user.id}/tasks/{task_id}",  # Original user's ID
        headers={"Authorization": f"Bearer {other_token}"}  # Other user's token
    )

    # This should fail due to user ID mismatch
    assert response.status_code == 403

    # Clean up other user
    with Session(engine) as session:
        session.delete(other_user)
        session.commit()


def test_task_validation_errors(client, setup_test_user_and_token):
    """Test validation errors for task creation"""
    user, token = setup_test_user_and_token

    # Test creating task without title (should fail)
    response = client.post(
        f"/api/{user.id}/tasks",
        json={},  # Empty - no title
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422  # Validation error


def test_pagination_and_filtering(client, setup_test_user_and_token):
    """Test pagination and filtering of tasks"""
    user, token = setup_test_user_and_token

    # Create multiple tasks
    for i in range(5):
        client.post(
            f"/api/{user.id}/tasks",
            json={
                "title": f"Task {i}",
                "priority": "high" if i % 2 == 0 else "low",
                "completed": i % 3 == 0
            },
            headers={"Authorization": f"Bearer {token}"}
        )

    # Test pagination
    response = client.get(
        f"/api/{user.id}/tasks?page=1&page_size=3",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["tasks"]) <= 3
    assert data["data"]["pagination"]["page"] == 1
    assert data["data"]["pagination"]["page_size"] == 3

    # Test filtering by priority
    response = client.get(
        f"/api/{user.id}/tasks?filter_priority=high",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    high_priority_count = len([t for t in data["data"]["tasks"] if t["priority"] == "high"])
    assert high_priority_count > 0