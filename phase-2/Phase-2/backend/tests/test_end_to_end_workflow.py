"""
End-to-End Workflow Tests for the Advanced Todo Application
Tests the complete user journey: registration -> login -> task management
"""
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
def setup_test_user():
    """Setup a test user in the database"""
    with Session(engine) as session:
        # Clean up any existing test users
        existing_users = session.exec(select(User).where(User.email.like("%test%@example.com"))).all()
        for user in existing_users:
            # Delete associated tasks first due to foreign key constraint
            tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
            for task in tasks:
                session.delete(task)
            session.delete(user)
        session.commit()

        # Create a test user
        user = User(
            email="e2e_test@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # "testpassword" hashed
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        yield user

        # Cleanup: delete the test user and associated tasks
        # Get fresh session for cleanup
        with Session(engine) as cleanup_session:
            # Delete associated tasks first due to foreign key constraint
            tasks = cleanup_session.exec(select(Task).where(Task.user_id == user.id)).all()
            for task in tasks:
                cleanup_session.delete(task)
            
            # Then delete the user
            user_to_delete = cleanup_session.get(User, user.id)
            if user_to_delete:
                cleanup_session.delete(user_to_delete)
            cleanup_session.commit()


def test_complete_user_workflow(client, setup_test_user):
    """Test the complete user workflow: login -> create task -> view task -> update -> delete"""
    user = setup_test_user
    
    # Step 1: Login to get token
    login_response = client.post("/auth/login", json={
        "email": "e2e_test@example.com",
        "password": "testpassword"
    })
    
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    login_data = login_response.json()
    assert "access_token" in login_data
    token = login_data["access_token"]
    
    # Step 2: Create a task using the user's ID from the token context
    # First, let's get the user ID by accessing the /auth/me endpoint
    me_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert me_response.status_code == 200
    user_data = me_response.json()
    user_id = user_data["id"]
    
    # Step 3: Create a task for this user
    create_task_response = client.post(
        f"/{user_id}/tasks",
        json={
            "title": "Test Task from Dashboard",
            "description": "Task created after successful login",
            "priority": "medium",
            "tags": ["dashboard", "test"],
            "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
            "recurring": "none"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert create_task_response.status_code == 201, f"Task creation failed: {create_task_response.text}"
    task_data = create_task_response.json()
    assert task_data["title"] == "Test Task from Dashboard"
    assert task_data["user_id"] == user_id
    task_id = task_data["id"]
    
    # Step 4: Get all tasks for the user to verify the task was created
    get_tasks_response = client.get(
        f"/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert get_tasks_response.status_code == 200, f"Getting tasks failed: {get_tasks_response.text}"
    tasks_data = get_tasks_response.json()
    assert tasks_data["success"] is True
    assert len(tasks_data["data"]["tasks"]) >= 1
    
    # Verify our task is in the list
    task_found = False
    for task in tasks_data["data"]["tasks"]:
        if task["id"] == task_id and task["title"] == "Test Task from Dashboard":
            task_found = True
            break
    assert task_found is True, f"Created task not found in task list. Response: {tasks_data}"
    
    # Step 5: Get the specific task
    get_task_response = client.get(
        f"/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert get_task_response.status_code == 200, f"Getting specific task failed: {get_task_response.text}"
    specific_task_data = get_task_response.json()
    assert specific_task_data["id"] == task_id
    assert specific_task_data["title"] == "Test Task from Dashboard"
    
    # Step 6: Update the task
    update_task_response = client.put(
        f"/{user_id}/tasks/{task_id}",
        json={
            "title": "Updated Test Task",
            "description": "Task has been updated",
            "priority": "high"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert update_task_response.status_code == 200, f"Task update failed: {update_task_response.text}"
    updated_task_data = update_task_response.json()
    assert updated_task_data["id"] == task_id
    assert updated_task_data["title"] == "Updated Test Task"
    assert updated_task_data["priority"] == "high"
    
    # Step 7: Toggle task completion
    toggle_response = client.patch(
        f"/{user_id}/tasks/{task_id}/complete",
        json={"completed": True},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert toggle_response.status_code == 200, f"Toggle completion failed: {toggle_response.text}"
    toggle_data = toggle_response.json()
    assert toggle_data["data"]["completed"] is True
    
    # Step 8: Delete the task
    delete_response = client.delete(
        f"/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert delete_response.status_code == 200, f"Task deletion failed: {delete_response.text}"
    delete_data = delete_response.json()
    assert delete_data["success"] is True
    
    # Step 9: Verify the task is deleted
    get_deleted_response = client.get(
        f"/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert get_deleted_response.status_code == 404, f"Task should be deleted but still accessible: {get_deleted_response.text}"


def test_multiple_tasks_workflow(client, setup_test_user):
    """Test creating multiple tasks after login"""
    user = setup_test_user
    
    # Login to get token
    login_response = client.post("/auth/login", json={
        "email": "e2e_test@example.com",
        "password": "testpassword"
    })
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Get user ID
    me_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert me_response.status_code == 200
    user_id = me_response.json()["id"]
    
    # Create multiple tasks
    task_ids = []
    for i in range(3):
        create_response = client.post(
            f"/{user_id}/tasks",
            json={
                "title": f"Test Task {i+1}",
                "description": f"Description for task {i+1}",
                "priority": "medium" if i % 2 == 0 else "high"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert create_response.status_code == 201, f"Failed to create task {i+1}: {create_response.text}"
        task_data = create_response.json()
        assert task_data["title"] == f"Test Task {i+1}"
        task_ids.append(task_data["id"])
    
    # Verify all tasks exist
    get_response = client.get(
        f"/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert get_response.status_code == 200
    tasks_data = get_response.json()
    assert len(tasks_data["data"]["tasks"]) >= 3
    
    # Verify all created tasks are present
    created_tasks = {task["id"]: task for task in tasks_data["data"]["tasks"]}
    for task_id in task_ids:
        assert task_id in created_tasks, f"Task {task_id} not found in retrieved tasks"
        assert created_tasks[task_id]["title"].startswith("Test Task")


def test_task_creation_immediately_after_login(client, setup_test_user):
    """Test that tasks can be created immediately after login without delay"""
    user = setup_test_user
    
    # Login
    login_response = client.post("/auth/login", json={
        "email": "e2e_test@example.com",
        "password": "testpassword"
    })
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Get user ID
    me_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert me_response.status_code == 200
    user_id = me_response.json()["id"]
    
    # Create task immediately after login
    task_response = client.post(
        f"/{user_id}/tasks",
        json={
            "title": "Immediate Task After Login",
            "description": "This task was created immediately after login",
            "priority": "high"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert task_response.status_code == 201, f"Immediate task creation failed: {task_response.text}"
    task_data = task_response.json()
    assert task_data["title"] == "Immediate Task After Login"
    assert task_data["user_id"] == user_id


def test_error_scenarios(client, setup_test_user):
    """Test various error scenarios in the workflow"""
    user = setup_test_user
    
    # Login to get token
    login_response = client.post("/auth/login", json={
        "email": "e2e_test@example.com",
        "password": "testpassword"
    })
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Get user ID
    me_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert me_response.status_code == 200
    user_id = me_response.json()["id"]
    
    # Test creating task with invalid data
    invalid_task_response = client.post(
        f"/{user_id}/tasks",
        json={  # Missing required title field
            "description": "Task without title should fail"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # This should fail with validation error (422) or succeed with default title
    # depending on how the API handles required fields
    # If it succeeds, the title should have a default value
    if invalid_task_response.status_code == 201:
        task_data = invalid_task_response.json()
        # If title is required, this means the API is providing a default title
        # which might be unexpected behavior
        assert "id" in task_data
    elif invalid_task_response.status_code == 422:
        # Expected validation error
        pass
    else:
        # Unexpected status code
        assert invalid_task_response.status_code in [201, 422], \
            f"Unexpected status code for invalid task: {invalid_task_response.status_code}"
    
    # Test accessing non-existent task
    fake_task_id = 999999
    get_fake_task_response = client.get(
        f"/{user_id}/tasks/{fake_task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert get_fake_task_response.status_code == 404, \
        f"Expected 404 for non-existent task, got {get_fake_task_response.status_code}"
    
    # Test updating non-existent task
    update_fake_task_response = client.put(
        f"/{user_id}/tasks/{fake_task_id}",
        json={"title": "Updated Fake Task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert update_fake_task_response.status_code == 404, \
        f"Expected 404 for updating non-existent task, got {update_fake_task_response.status_code}"
    
    # Test deleting non-existent task
    delete_fake_task_response = client.delete(
        f"/{user_id}/tasks/{fake_task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert delete_fake_task_response.status_code == 404, \
        f"Expected 404 for deleting non-existent task, got {delete_fake_task_response.status_code}"


def test_user_isolation_after_login(client, setup_test_user):
    """Test that user isolation works correctly after login"""
    user = setup_test_user
    
    # Login as first user
    login_response = client.post("/auth/login", json={
        "email": "e2e_test@example.com",
        "password": "testpassword"
    })
    
    assert login_response.status_code == 200
    token1 = login_response.json()["access_token"]
    
    # Get first user ID
    me_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token1}"
    })
    assert me_response.status_code == 200
    user1_id = me_response.json()["id"]
    
    # Create a second user directly in the database
    with Session(engine) as session:
        user2 = User(
            email="second_user@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # "testpassword" hashed
        )
        session.add(user2)
        session.commit()
        session.refresh(user2)
        
        # Login as second user
        login_response2 = client.post("/auth/login", json={
            "email": "second_user@example.com",
            "password": "testpassword"
        })
        
        assert login_response2.status_code == 200
        token2 = login_response2.json()["access_token"]
        
        # Create a task for user2
        create_task_response = client.post(
            f"/{user2.id}/tasks",
            json={"title": "User 2 Task"},
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        assert create_task_response.status_code == 201
        user2_task_id = create_task_response.json()["id"]
    
    # Now try to access user2's task using user1's token and user2's ID
    # This should fail due to token-user mismatch
    access_response = client.get(
        f"/{user2.id}/tasks/{user2_task_id}",  # user2's task
        headers={"Authorization": f"Bearer {token1}"}  # user1's token
    )
    
    # This should fail with 403 (Forbidden) due to user ID mismatch
    assert access_response.status_code == 403, \
        f"Expected 403 for cross-user access, got {access_response.status_code}: {access_response.text}"
    
    # Clean up: delete second user and their tasks
    with Session(engine) as session:
        # Delete user2's tasks first
        user2_tasks = session.exec(select(Task).where(Task.user_id == user2.id)).all()
        for task in user2_tasks:
            session.delete(task)
        
        # Delete user2
        session.delete(user2)
        session.commit()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])