"""
Debug script to test the backend authentication and user validation flow
"""
from fastapi.testclient import TestClient
from src.main import app
import json

def test_backend_flow():
    client = TestClient(app)
    
    print("=== Testing Backend Authentication Flow ===\n")
    
    # Step 1: Register a new user
    print("1. Registering a new user...")
    register_response = client.post("/auth/register", json={
        "email": "debug.test@example.com",
        "password": "SecurePass123!"
    })
    
    print(f"   Registration status: {register_response.status_code}")
    if register_response.status_code != 200:
        print(f"   Registration failed: {register_response.text}")
        return False
    
    register_data = register_response.json()
    print(f"   Registration successful: {register_data}")
    token = register_data.get("access_token")
    
    # Step 2: Get user profile (tests get_current_user_id function)
    print("\n2. Getting user profile (tests get_current_user_id function)...")
    profile_response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    print(f"   Profile status: {profile_response.status_code}")
    if profile_response.status_code != 200:
        print(f"   Profile request failed: {profile_response.text}")
        print("   This indicates an issue with user validation in get_current_user_id")
        return False
    
    profile_data = profile_response.json()
    user_id = profile_data.get("id")
    print(f"   Profile retrieved successfully: User ID = {user_id}")
    
    # Step 3: Try to create a task (the failing step)
    print(f"\n3. Creating a task for user {user_id}...")
    task_response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Debug Test Task",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"   Task creation status: {task_response.status_code}")
    if task_response.status_code != 201:
        print(f"   Task creation failed: {task_response.text}")
        print("   This confirms the issue is in the task creation validation")
        return False
    
    task_data = task_response.json()
    print(f"   Task created successfully: {task_data}")
    
    print("\n✓ All steps completed successfully!")
    return True

if __name__ == "__main__":
    success = test_backend_flow()
    if success:
        print("\n🎉 Backend authentication flow is working correctly!")
    else:
        print("\n❌ Backend authentication flow has issues!")