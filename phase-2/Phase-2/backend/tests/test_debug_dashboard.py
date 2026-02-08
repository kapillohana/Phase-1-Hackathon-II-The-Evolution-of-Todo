"""
Debug test to identify the specific issue with task creation after login
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
        existing_users = session.exec(select(User).where(User.email.like("%debug%@example.com"))).all()
        for user in existing_users:
            # Delete associated tasks first due to foreign key constraint
            tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
            for task in tasks:
                session.delete(task)
            session.delete(user)
        session.commit()

        # Create a test user
        user = User(
            email="debug_test@example.com",
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


def test_debug_task_creation(client, setup_test_user):
    """
    Debug the exact issue with task creation after login
    """
    user = setup_test_user
    
    print("\n=== DEBUG: Task Creation After Login ===")
    
    # Step 1: Login
    print("1. Logging in...")
    login_response = client.post("/auth/login", json={
        "email": "debug_test@example.com",
        "password": "testpassword"
    })
    
    print(f"   Login status: {login_response.status_code}")
    if login_response.status_code != 200:
        print(f"   Login failed: {login_response.text}")
        return  # Early return to prevent further errors
    
    login_data = login_response.json()
    token = login_data["access_token"]
    print(f"   Token received: {token[:20]}...")
    
    # Step 2: Get user ID
    print("2. Getting user profile...")
    me_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    print(f"   Profile status: {me_response.status_code}")
    user_data = me_response.json()
    user_id = user_data["id"]
    print(f"   User ID: {user_id}")
    
    # Step 3: Try to create a task with various data formats
    print("3. Testing task creation with different data formats...")
    
    # Test 1: Basic task creation
    print("   Test 1: Basic task")
    basic_task_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "Basic Task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"     Status: {basic_task_response.status_code}")
    if basic_task_response.status_code != 201:
        print(f"     Error: {basic_task_response.text}")
    else:
        basic_task = basic_task_response.json()
        print(f"     Created task ID: {basic_task.get('id')}")
    
    # Test 2: Task with tags as array (this might be the issue!)
    print("   Test 2: Task with tags as array")
    tag_task_response = client.post(
        f"/{user_id}/tasks",
        json={
            "title": "Task with Tags",
            "tags": ["work", "important", "test"]  # Tags as array
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"     Status: {tag_task_response.status_code}")
    if tag_task_response.status_code != 201:
        print(f"     Error: {tag_task_response.text}")
        print(f"     This might be the source of the dashboard issue!")
    else:
        tag_task = tag_task_response.json()
        print(f"     Created task ID: {tag_task.get('id')}")
        print(f"     Tags in response: {tag_task.get('tags')}")
    
    # Test 3: Task with all fields
    print("   Test 3: Task with all fields")
    full_task_response = client.post(
        f"/{user_id}/tasks",
        json={
            "title": "Full Task",
            "description": "A task with all fields filled",
            "priority": "high",
            "tags": ["full", "test", "complete"],
            "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
            "recurring": "none"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"     Status: {full_task_response.status_code}")
    if full_task_response.status_code != 201:
        print(f"     Error: {full_task_response.text}")
    else:
        full_task = full_task_response.json()
        print(f"     Created task ID: {full_task.get('id')}")
        print(f"     Title: {full_task.get('title')}")
        print(f"     Tags: {full_task.get('tags')}")
        print(f"     Priority: {full_task.get('priority')}")
    
    # Step 4: Get all tasks to verify they were created
    print("4. Getting all tasks to verify creation...")
    get_tasks_response = client.get(
        f"/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"   Get tasks status: {get_tasks_response.status_code}")
    
    if get_tasks_response.status_code == 200:
        tasks_data = get_tasks_response.json()
        print(f"   Number of tasks: {len(tasks_data['data']['tasks']) if 'data' in tasks_data and 'tasks' in tasks_data['data'] else 0}")
        
        for i, task in enumerate(tasks_data['data']['tasks']):
            print(f"     Task {i+1}: {task.get('title')} (ID: {task.get('id')}) - Tags: {task.get('tags')}")
    else:
        print(f"   Failed to get tasks: {get_tasks_response.text}")


def test_specific_dashboard_scenario(client, setup_test_user):
    """
    Test the exact scenario that happens in the dashboard
    """
    user = setup_test_user
    
    print("\n=== REPLICATING DASHBOARD SCENARIO ===")
    
    # Simulate the exact sequence that happens in the dashboard
    print("Step 1: User logs in")
    login_resp = client.post("/auth/login", json={
        "email": "debug_test@example.com",
        "password": "testpassword"
    })
    
    if login_resp.status_code != 200:
        print(f"Login failed: {login_resp.text}")
        return
    
    token = login_resp.json()["access_token"]
    print(f"Token obtained: {token[:10]}...")
    
    print("Step 2: Dashboard loads user profile")
    profile_resp = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    if profile_resp.status_code != 200:
        print(f"Profile load failed: {profile_resp.text}")
        return
    
    user_id = profile_resp.json()["id"]
    print(f"User ID obtained: {user_id}")
    
    print("Step 3: Dashboard loads existing tasks")
    tasks_resp = client.get(
        f"/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if tasks_resp.status_code != 200:
        print(f"Tasks load failed: {tasks_resp.text}")
        return
    
    initial_count = len(tasks_resp.json()["data"]["tasks"])
    print(f"Initial task count: {initial_count}")
    
    print("Step 4: User clicks 'Add Task' in dashboard")
    print("Step 5: User fills task form and submits")
    
    # This is where the issue likely occurs
    new_task_resp = client.post(
        f"/{user_id}/tasks",
        json={
            "title": "Task Created in Dashboard",
            "description": "This task was created after login in the dashboard",
            "priority": "medium",
            "tags": ["dashboard", "new", "test"],
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "recurring": "none"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Task creation status: {new_task_resp.status_code}")
    
    if new_task_resp.status_code != 201:
        print(f"❌ TASK CREATION FAILED!")
        print(f"Status: {new_task_resp.status_code}")
        print(f"Response: {new_task_resp.text}")
        print(f"Headers sent: Authorization: Bearer {token[:20]}...")
        print(f"Body sent: {{'title': 'Task Created in Dashboard', 'tags': ['dashboard', 'new', 'test'], ...}}")
        
        # Let's try with different tag formats to see what works
        print("\nTrying alternative tag formats...")
        
        # Try with tags as JSON string
        alt_task_resp = client.post(
            f"/{user_id}/tasks",
            json={
                "title": "Alternative Format Task",
                "tags": '["alt", "format", "test"]'  # String instead of array
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"Alternative format status: {alt_task_resp.status_code}")
        if alt_task_resp.status_code != 201:
            print(f"Alternative also failed: {alt_task_resp.text}")
        
        return
    else:
        print("✅ Task created successfully!")
        new_task = new_task_resp.json()
        print(f"New task ID: {new_task['id']}")
        print(f"New task title: {new_task['title']}")
        print(f"New task tags: {new_task['tags']}")
    
    print("Step 6: Dashboard refreshes task list")
    refresh_resp = client.get(
        f"/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if refresh_resp.status_code != 200:
        print(f"Refresh failed: {refresh_resp.text}")
        return
    
    final_count = len(refresh_resp.json()["data"]["tasks"])
    print(f"Final task count: {final_count}")
    print(f"Count increased by: {final_count - initial_count}")
    
    # Check if our new task is in the list
    new_task_in_list = any(
        task["id"] == new_task["id"] and task["title"] == new_task["title"]
        for task in refresh_resp.json()["data"]["tasks"]
    )
    
    if new_task_in_list:
        print("✅ New task appears in refreshed list!")
    else:
        print("❌ New task does not appear in refreshed list!")
        print("This indicates a potential issue with task persistence or retrieval.")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])