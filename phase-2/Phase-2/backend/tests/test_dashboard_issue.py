"""
Specific tests to replicate the issue with adding tasks after login
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
        existing_users = session.exec(select(User).where(User.email.like("%dashboard%@example.com"))).all()
        for user in existing_users:
            # Delete associated tasks first due to foreign key constraint
            tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
            for task in tasks:
                session.delete(task)
            session.delete(user)
        session.commit()

        # Create a test user
        user = User(
            email="dashboard_test@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # "testpassword" hashed
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        yield user

        # Cleanup: delete the test user and associated tasks
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


def test_dashboard_task_creation_scenario(client, setup_test_user):
    """
    Test the specific scenario: login -> go to dashboard -> add task
    This replicates the issue you experienced
    """
    user = setup_test_user
    
    print("\n=== Testing Dashboard Task Creation Scenario ===")
    
    # Step 1: Login (simulating user login)
    print("Step 1: Logging in...")
    login_response = client.post("/auth/login", json={
        "email": "dashboard_test@example.com",
        "password": "testpassword"
    })
    
    print(f"Login status: {login_response.status_code}")
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        assert False, f"Login failed with status {login_response.status_code}: {login_response.text}"
    
    login_data = login_response.json()
    assert "access_token" in login_data
    token = login_data["access_token"]
    print(f"Received token: {token[:20]}..." if token else "No token received")
    
    # Step 2: Get user profile (simulating dashboard load)
    print("\nStep 2: Loading dashboard (getting user profile)...")
    me_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    print(f"Get user profile status: {me_response.status_code}")
    if me_response.status_code != 200:
        print(f"Get user profile failed: {me_response.text}")
        assert False, f"Get user profile failed: {me_response.text}"
    
    user_data = me_response.json()
    user_id = user_data["id"]
    print(f"User ID: {user_id}")
    
    # Step 3: Get existing tasks (simulating dashboard task list load)
    print("\nStep 3: Loading existing tasks...")
    get_tasks_response = client.get(
        f"/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Get tasks status: {get_tasks_response.status_code}")
    if get_tasks_response.status_code != 200:
        print(f"Get tasks failed: {get_tasks_response.text}")
        assert False, f"Get tasks failed: {get_tasks_response.text}"
    
    tasks_data = get_tasks_response.json()
    initial_task_count = len(tasks_data["data"]["tasks"]) if "data" in tasks_data and "tasks" in tasks_data["data"] else 0
    print(f"Initial task count: {initial_task_count}")
    
    # Step 4: Add a new task from dashboard (the problematic step)
    print("\nStep 4: Adding new task from dashboard...")
    new_task_data = {
        "title": "Dashboard Task - Created After Login",
        "description": "This task was added after successful login and dashboard load",
        "priority": "medium",
        "tags": ["dashboard", "after-login"],
        "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
        "recurring": "none"
    }
    
    create_task_response = client.post(
        f"/{user_id}/tasks",
        json=new_task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Create task status: {create_task_response.status_code}")
    print(f"Response text: {create_task_response.text}")
    
    # This is the critical assertion - if this fails, it's the issue you experienced
    if create_task_response.status_code != 201:
        print(f"\n*** FAILURE: Task creation failed ***")
        print(f"Status code: {create_task_response.status_code}")
        print(f"Response: {create_task_response.text}")
        print(f"Headers sent: Authorization: Bearer {token[:20]}...")
        print(f"Data sent: {new_task_data}")
        assert create_task_response.status_code == 201, f"Task creation failed: {create_task_response.text}"
    
    created_task = create_task_response.json()
    print(f"Task created successfully with ID: {created_task.get('id')}")
    print(f"Created task title: {created_task.get('title')}")
    
    # Step 5: Verify the task was actually created
    print("\nStep 5: Verifying task was created...")
    verify_tasks_response = client.get(
        f"/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Verify tasks status: {verify_tasks_response.status_code}")
    if verify_tasks_response.status_code != 200:
        print(f"Verify tasks failed: {verify_tasks_response.text}")
        assert False, f"Verify tasks failed: {verify_tasks_response.text}"
    
    verify_tasks_data = verify_tasks_response.json()
    final_task_count = len(verify_tasks_data["data"]["tasks"]) if "data" in verify_tasks_data and "tasks" in verify_tasks_data["data"] else 0
    print(f"Final task count: {final_task_count}")
    
    # Verify the new task exists in the list
    new_task_exists = False
    for task in verify_tasks_data["data"]["tasks"]:
        if task.get("id") == created_task.get("id") and task.get("title") == created_task.get("title"):
            new_task_exists = True
            print(f"✓ Verified task exists in task list: {task.get('title')}")
            break
    
    if not new_task_exists:
        print(f"\n*** FAILURE: Created task not found in task list ***")
        print(f"Looking for task ID: {created_task.get('id')}")
        print(f"Looking for title: {created_task.get('title')}")
        print(f"All retrieved tasks: {[t.get('title') for t in verify_tasks_data['data']['tasks']]}")
        assert False, "Created task was not found in the task list after creation"
    
    print(f"\n✓ Successfully created and verified task after login!")
    print(f"Task count increased from {initial_task_count} to {final_task_count}")


def test_concurrent_operations_after_login(client, setup_test_user):
    """
    Test multiple operations happening in quick succession after login
    This might reveal race conditions or timing issues
    """
    user = setup_test_user
    
    print("\n=== Testing Concurrent Operations After Login ===")
    
    # Login
    login_response = client.post("/auth/login", json={
        "email": "dashboard_test@example.com",
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
    
    # Simulate rapid-fire operations that might happen in a dashboard
    operations_results = []
    
    # Operation 1: Get tasks
    op1 = client.get(f"/{user_id}/tasks", headers={"Authorization": f"Bearer {token}"})
    operations_results.append(("get_tasks", op1.status_code, op1.text))
    
    # Operation 2: Create task
    op2 = client.post(
        f"/{user_id}/tasks",
        json={"title": "Rapid Task 1", "priority": "low"},
        headers={"Authorization": f"Bearer {token}"}
    )
    operations_results.append(("create_task", op2.status_code, op2.text))
    
    # Operation 3: Get tasks again
    op3 = client.get(f"/{user_id}/tasks", headers={"Authorization": f"Bearer {token}"})
    operations_results.append(("get_tasks_2", op3.status_code, op3.text))
    
    # Operation 4: Create another task
    op4 = client.post(
        f"/{user_id}/tasks",
        json={"title": "Rapid Task 2", "priority": "high"},
        headers={"Authorization": f"Bearer {token}"}
    )
    operations_results.append(("create_task_2", op4.status_code, op4.text))
    
    # Check results
    for op_name, status, text in operations_results:
        print(f"{op_name}: {status}")
        if status not in [200, 201]:
            print(f"  ERROR: {text}")
    
    # Critical: Both task creations should succeed
    create_op_statuses = [status for op_name, status, _ in operations_results if "create_task" in op_name]
    for i, status in enumerate(create_op_statuses):
        assert status == 201, f"Task creation {i+1} failed with status {status}: {[t for n, s, t in operations_results if 'create_task' in n][i]}"
    
    print("✓ All rapid operations succeeded")


def test_token_expiry_and_refresh_simulation(client, setup_test_user):
    """
    Test if there are issues with token handling during task creation
    """
    user = setup_test_user
    
    print("\n=== Testing Token Handling During Task Creation ===")
    
    # Login
    login_response = client.post("/auth/login", json={
        "email": "dashboard_test@example.com",
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
    
    # Test with valid token
    valid_token_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "Valid Token Task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Valid token task creation: {valid_token_response.status_code}")
    assert valid_token_response.status_code == 201, f"Valid token task creation failed: {valid_token_response.text}"
    
    # Test with malformed token
    malformed_token_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "Malformed Token Task"},
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    
    print(f"Malformed token task creation: {malformed_token_response.status_code}")
    assert malformed_token_response.status_code in [401, 422], "Malformed token should be rejected"
    
    # Test with no token
    no_token_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "No Token Task"}
        # No authorization header
    )
    
    print(f"No token task creation: {no_token_response.status_code}")
    assert no_token_response.status_code == 401, "Missing token should be rejected"


def test_edge_cases_in_task_creation(client, setup_test_user):
    """
    Test edge cases that might cause issues with task creation
    """
    user = setup_test_user
    
    print("\n=== Testing Edge Cases in Task Creation ===")
    
    # Login
    login_response = client.post("/auth/login", json={
        "email": "dashboard_test@example.com",
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
    
    # Test with minimal data
    minimal_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "Minimal Task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Minimal task creation: {minimal_response.status_code}")
    assert minimal_response.status_code == 201, f"Minimal task creation failed: {minimal_response.text}"
    
    # Test with maximum data
    max_data_response = client.post(
        f"/{user_id}/tasks",
        json={
            "title": "Maximum Data Task",
            "description": "This is a detailed description with lots of information about the task that needs to be completed.",
            "priority": "high",
            "tags": ["tag1", "tag2", "tag3", "important", "urgent"],
            "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "recurring": "daily"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Maximum data task creation: {max_data_response.status_code}")
    assert max_data_response.status_code == 201, f"Maximum data task creation failed: {max_data_response.text}"
    
    # Test with empty strings and null values where allowed
    edge_case_response = client.post(
        f"/{user_id}/tasks",
        json={
            "title": "Edge Case Task",
            "description": "",  # Empty description should be OK
            "priority": "medium",
            "tags": [],  # Empty tags should be OK
            "due_date": None,  # Null due date should be OK
            "recurring": "none"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Edge case task creation: {edge_case_response.status_code}")
    assert edge_case_response.status_code == 201, f"Edge case task creation failed: {edge_case_response.text}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])