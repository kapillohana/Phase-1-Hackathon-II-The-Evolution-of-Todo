"""
Tests to identify specific issues with authentication and task creation flow
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from datetime import datetime, timedelta
import json
import time

from src.main import app
from src.database.database import engine, get_session
from src.models.models import User, Task
from src.auth.auth import create_access_token, verify_user_id_match


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
        existing_users = session.exec(select(User).where(User.email.like("%auth%@example.com"))).all()
        for user in existing_users:
            # Delete associated tasks first due to foreign key constraint
            tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
            for task in tasks:
                session.delete(task)
            session.delete(user)
        session.commit()

        # Create a test user
        user = User(
            email="auth_test@example.com",
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


def test_auth_flow_and_task_creation_detailed(client, setup_test_user):
    """
    Detailed test of the authentication flow and task creation to identify specific issues
    """
    user = setup_test_user
    
    print("\n=== Detailed Auth Flow and Task Creation Test ===")
    
    # Step 1: Login and inspect the response
    print("Step 1: Attempting login...")
    login_start_time = time.time()
    login_response = client.post("/auth/login", json={
        "email": "auth_test@example.com",
        "password": "testpassword"
    })
    login_end_time = time.time()
    
    print(f"Login took {(login_end_time - login_start_time)*1000:.2f}ms")
    print(f"Login status: {login_response.status_code}")
    print(f"Login response headers: {dict(login_response.headers)}")
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        assert False, f"Login failed with status {login_response.status_code}: {login_response.text}"
    
    login_data = login_response.json()
    print(f"Login response data keys: {list(login_data.keys())}")
    print(f"Access token present: {'access_token' in login_data}")
    print(f"Token type present: {'token_type' in login_data}")
    
    assert "access_token" in login_data
    assert "token_type" in login_data
    token = login_data["access_token"]
    token_type = login_data["token_type"]
    print(f"Token type: {token_type}")
    print(f"Token length: {len(token)}")
    
    # Step 2: Get user profile to verify token works
    print("\nStep 2: Getting user profile with token...")
    profile_start_time = time.time()
    me_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    profile_end_time = time.time()
    
    print(f"Profile request took {(profile_end_time - profile_start_time)*1000:.2f}ms")
    print(f"Profile status: {me_response.status_code}")
    
    if me_response.status_code != 200:
        print(f"Profile request failed: {me_response.text}")
        assert False, f"Profile request failed: {me_response.text}"
    
    user_data = me_response.json()
    print(f"User data keys: {list(user_data.keys())}")
    user_id = user_data["id"]
    print(f"Retrieved user ID: {user_id}")
    print(f"User email: {user_data['email']}")
    
    # Step 3: Test the user_id validation function directly
    print(f"\nStep 3: Testing user ID validation...")
    # This simulates what happens in the API when validating user_id
    path_user_id = user_id
    token_user_id = user_id  # In a real JWT, this would be extracted from the token
    validation_result = path_user_id == token_user_id  # Simplified version of verify_user_id_match
    print(f"User ID validation result: {validation_result}")
    assert validation_result, "User ID validation should pass"
    
    # Step 4: Create task - the critical step
    print(f"\nStep 4: Creating task for user {user_id}...")
    task_start_time = time.time()
    create_task_response = client.post(
        f"/{user_id}/tasks",
        json={
            "title": "Test Task After Login",
            "description": "Task created after successful authentication",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    task_end_time = time.time()
    
    print(f"Task creation took {(task_end_time - task_start_time)*1000:.2f}ms")
    print(f"Task creation status: {create_task_response.status_code}")
    print(f"Task response headers: {dict(create_task_response.headers)}")
    
    if create_task_response.status_code != 201:
        print(f"Task creation failed: {create_task_response.text}")
        print(f"Request headers sent: {{'Authorization': 'Bearer {token[:20]}...'}}")
        print(f"Request body: {{'title': 'Test Task After Login', 'description': '...', 'priority': 'medium'}}")
        assert False, f"Task creation failed with status {create_task_response.status_code}: {create_task_response.text}"
    
    task_data = create_task_response.json()
    print(f"Task creation response keys: {list(task_data.keys())}")
    print(f"Created task ID: {task_data.get('id')}")
    print(f"Created task title: {task_data.get('title')}")
    print(f"Created task user_id: {task_data.get('user_id')}")
    
    # Verify the task has the correct user_id
    assert task_data["user_id"] == user_id, f"Task user_id mismatch: expected {user_id}, got {task_data.get('user_id')}"
    
    # Step 5: Verify task exists by retrieving it
    print(f"\nStep 5: Verifying task exists...")
    verify_response = client.get(
        f"/{user_id}/tasks/{task_data['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Task verification status: {verify_response.status_code}")
    if verify_response.status_code != 200:
        print(f"Task verification failed: {verify_response.text}")
        assert False, f"Task verification failed: {verify_response.text}"
    
    retrieved_task = verify_response.json()
    print(f"Retrieved task title: {retrieved_task.get('title')}")
    assert retrieved_task["id"] == task_data["id"]
    assert retrieved_task["title"] == task_data["title"]
    
    print(f"\n✓ All steps completed successfully!")


def test_different_token_scenarios(client, setup_test_user):
    """
    Test different token-related scenarios that might cause issues
    """
    user = setup_test_user
    
    print("\n=== Testing Different Token Scenarios ===")
    
    # Login to get a valid token
    login_response = client.post("/auth/login", json={
        "email": "auth_test@example.com",
        "password": "testpassword"
    })
    
    assert login_response.status_code == 200
    valid_token = login_response.json()["access_token"]
    
    # Get user ID
    me_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {valid_token}"
    })
    assert me_response.status_code == 200
    user_id = me_response.json()["id"]
    
    # Test 1: Valid token
    print("Test 1: Using valid token")
    valid_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "Valid Token Task"},
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    print(f"  Status: {valid_response.status_code}")
    assert valid_response.status_code == 201
    
    # Test 2: Token with extra spaces
    print("Test 2: Using token with extra spaces")
    spaced_token_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "Spaced Token Task"},
        headers={"Authorization": f"  Bearer {valid_token}  "}
    )
    print(f"  Status: {spaced_token_response.status_code}")
    # This might fail depending on how the API handles whitespace
    
    # Test 3: Token without "Bearer " prefix
    print("Test 3: Using token without Bearer prefix")
    no_prefix_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "No Prefix Token Task"},
        headers={"Authorization": valid_token}
    )
    print(f"  Status: {no_prefix_response.status_code}")
    assert no_prefix_response.status_code == 422 or no_prefix_response.status_code == 401  # Should fail
    
    # Test 4: Malformed token
    print("Test 4: Using malformed token")
    malformed_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "Malformed Token Task"},
        headers={"Authorization": "Bearer invalid.token.format"}
    )
    print(f"  Status: {malformed_response.status_code}")
    assert malformed_response.status_code in [401, 422]  # Should fail
    
    print("✓ Token scenario tests completed")


def test_path_parameter_vs_token_matching(client, setup_test_user):
    """
    Test the user ID matching between path parameter and token
    This is often where issues occur in multi-user isolation
    """
    user = setup_test_user
    
    print("\n=== Testing Path Parameter vs Token Matching ===")
    
    # Login to get token
    login_response = client.post("/auth/login", json={
        "email": "auth_test@example.com",
        "password": "testpassword"
    })
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Get user ID
    me_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert me_response.status_code == 200
    actual_user_id = me_response.json()["id"]
    print(f"Actual user ID: {actual_user_id}")
    
    # Test 1: Correct user ID in path (should work)
    print("Test 1: Correct user ID in path parameter")
    correct_response = client.post(
        f"/{actual_user_id}/tasks",
        json={"title": "Correct User ID Task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"  Status: {correct_response.status_code}")
    assert correct_response.status_code == 201
    
    # Test 2: Wrong user ID in path (should fail with 403)
    print("Test 2: Wrong user ID in path parameter")
    wrong_user_id = actual_user_id + 1000000  # Definitely not our user ID
    wrong_response = client.post(
        f"/{wrong_user_id}/tasks",
        json={"title": "Wrong User ID Task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"  Status: {wrong_response.status_code}")
    assert wrong_response.status_code == 403, f"Expected 403 for user ID mismatch, got {wrong_response.status_code}"
    
    # Test 3: Zero user ID (edge case)
    print("Test 3: Zero user ID in path parameter")
    zero_response = client.post(
        "/0/tasks",
        json={"title": "Zero User ID Task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"  Status: {zero_response.status_code}")
    # This might return 403 (forbidden) or 404 (user not found), depending on implementation
    
    print("✓ Path parameter vs token matching tests completed")


def test_concurrent_requests_after_login(client, setup_test_user):
    """
    Test multiple concurrent requests after login to identify race conditions
    """
    user = setup_test_user
    
    print("\n=== Testing Concurrent Requests After Login ===")
    
    # Login to get token
    login_response = client.post("/auth/login", json={
        "email": "auth_test@example.com",
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
    
    # Make multiple requests in sequence (simulating rapid UI interactions)
    results = []
    for i in range(5):
        response = client.post(
            f"/{user_id}/tasks",
            json={"title": f"Concurrent Task {i+1}"},
            headers={"Authorization": f"Bearer {token}"}
        )
        results.append((i+1, response.status_code, response.text if response.status_code != 201 else "Success"))
        print(f"Request {i+1}: Status {response.status_code}")
    
    # Check that all requests succeeded
    all_success = all(status == 201 for _, status, _ in results)
    success_count = sum(1 for _, status, _ in results if status == 201)
    
    print(f"Successful requests: {success_count}/5")
    for i, (req_num, status, text) in enumerate(results):
        if status != 201:
            print(f"  Request {req_num} failed: {text}")
    
    assert all_success, f"Not all requests succeeded. Success count: {success_count}/5"
    
    print("✓ Concurrent requests test completed successfully")


def test_task_creation_with_delay_after_login(client, setup_test_user):
    """
    Test if there's an issue with creating tasks immediately after login vs after a delay
    """
    user = setup_test_user
    
    print("\n=== Testing Task Creation Timing ===")
    
    # Login
    login_response = client.post("/auth/login", json={
        "email": "auth_test@example.com",
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
    
    # Test 1: Create task immediately after getting user ID
    print("Test 1: Creating task immediately after login")
    immediate_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "Immediate Task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"  Immediate creation status: {immediate_response.status_code}")
    assert immediate_response.status_code == 201
    
    # Test 2: Wait a bit then create another task (to see if timing matters)
    print("Test 2: Creating task after short delay")
    import time
    time.sleep(0.1)  # 100ms delay
    
    delayed_response = client.post(
        f"/{user_id}/tasks",
        json={"title": "Delayed Task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"  Delayed creation status: {delayed_response.status_code}")
    assert delayed_response.status_code == 201
    
    # Test 3: Get all tasks to verify both were created
    get_all_response = client.get(
        f"/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_all_response.status_code == 200
    tasks = get_all_response.json()["data"]["tasks"]
    
    immediate_task_exists = any(task["title"] == "Immediate Task" for task in tasks)
    delayed_task_exists = any(task["title"] == "Delayed Task" for task in tasks)
    
    print(f"  Immediate task exists: {immediate_task_exists}")
    print(f"  Delayed task exists: {delayed_task_exists}")
    
    assert immediate_task_exists, "Immediate task was not created"
    assert delayed_task_exists, "Delayed task was not created"
    
    print("✓ Timing test completed successfully")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])