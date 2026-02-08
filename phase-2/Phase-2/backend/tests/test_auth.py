import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from jose import jwt
from sqlmodel import Session, select
import os
from datetime import datetime, timedelta

from src.main import app
from src.database.database import engine, get_session
from src.models.models import User
from src.auth.auth import SECRET_KEY, ALGORITHM, create_access_token


@pytest.fixture(scope="module")
def client():
    """Create a test client for the API"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def setup_test_user():
    """Setup a test user in the database"""
    # Create a test user in the database
    with Session(engine) as session:
        # Check if user already exists to avoid conflicts
        existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()
        if existing_user:
            session.delete(existing_user)
            session.commit()

        user = User(
            email="test@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # "testpassword" hashed
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        yield user

        # Cleanup: delete the test user
        session.delete(user)
        session.commit()


def test_login_success(client, setup_test_user):
    """Test successful user login"""
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify token is valid
    token = data["access_token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "user_id" in payload
    assert "email" in payload
    assert payload["email"] == "test@example.com"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_login_missing_fields(client):
    """Test login with missing fields"""
    response = client.post("/api/auth/login", json={
        "email": "test@example.com"
        # Missing password
    })

    assert response.status_code == 422  # Validation error


def test_register_new_user(client):
    """Test registering a new user"""
    response = client.post("/api/auth/register", json={
        "email": "newuser@example.com",
        "password": "newpassword123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "newuser@example.com"

    # Verify user was created in database
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == "newuser@example.com")).first()
        assert user is not None
        assert user.email == "newuser@example.com"


def test_register_duplicate_email(client, setup_test_user):
    """Test registering with duplicate email"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",  # Already exists
        "password": "anotherpassword"
    })

    assert response.status_code == 400  # Email already registered


def test_get_current_user(client, setup_test_user):
    """Test getting current user profile with valid token"""
    # First login to get token
    login_response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Get current user with token
    response = client.get("/api/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token"""
    response = client.get("/api/auth/me", headers={
        "Authorization": "Bearer invalidtoken"
    })

    assert response.status_code == 401


def test_logout(client, setup_test_user):
    """Test user logout"""
    # Login first
    login_response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Logout
    response = client.post("/api/auth/logout", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Successfully logged out"