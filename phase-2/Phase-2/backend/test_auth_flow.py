"""
Simple test to verify the registration and login flow
"""
from fastapi.testclient import TestClient
from src.main import app

def test_registration_and_login():
    client = TestClient(app)
    
    print("=== Testing Registration and Login Flow ===")
    
    # First, try to register a new user
    print("\n1. Registering a new user...")
    register_response = client.post("/auth/register", json={
        "email": "dashboard.test@example.com",
        "password": "SecurePass123!"
    })
    
    print(f"   Register status: {register_response.status_code}")
    if register_response.status_code == 200:
        register_data = register_response.json()
        print(f"   Registration successful: {register_data}")
        user_id = register_data.get('id')
        print(f"   User ID: {user_id}")
    else:
        print(f"   Registration failed: {register_response.text}")
        # If registration fails due to user already existing, try to log in directly
        print("   Trying to log in with existing user...")
    
    # Then try to log in
    print("\n2. Logging in...")
    login_response = client.post("/auth/login", json={
        "email": "dashboard.test@example.com",
        "password": "SecurePass123!"
    })
    
    print(f"   Login status: {login_response.status_code}")
    if login_response.status_code == 200:
        login_data = login_response.json()
        print(f"   Login successful: {login_data}")
        token = login_data.get("access_token")
        print(f"   Token: {token[:20]}..." if token else "No token")
        
        # Get user ID from profile
        print("\n3. Getting user profile...")
        profile_response = client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        
        print(f"   Profile status: {profile_response.status_code}")
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print(f"   Profile: {profile_data}")
            user_id = profile_data.get("id")
            
            # Now try to create a task
            print(f"\n4. Creating task for user {user_id}...")
            task_response = client.post(
                f"/{user_id}/tasks",
                json={
                    "title": "Test Task from Dashboard",
                    "description": "Task created after successful login",
                    "priority": "medium",
                    "tags": ["dashboard", "test"],
                    "recurring": "none"
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            
            print(f"   Task creation status: {task_response.status_code}")
            if task_response.status_code == 201:
                task_data = task_response.json()
                print(f"   Task created successfully: {task_data}")
            else:
                print(f"   Task creation failed: {task_response.text}")
        else:
            print(f"   Profile request failed: {profile_response.text}")
    else:
        print(f"   Login failed: {login_response.text}")
        print("   This explains why dashboard task creation doesn't work!")
        print("   The issue is with authentication, not task creation.")

if __name__ == "__main__":
    test_registration_and_login()