"""
Authentication module for the Advanced Todo Application
Handles JWT token creation, verification, and user authentication
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel import Session
from pydantic import BaseModel
import os
from ..database.database import get_session
from ..models.models import User

# Get the JWT secret from environment variables
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Security scheme for API docs
security = HTTPBearer()


class TokenData(BaseModel):
    """
    Data contained in JWT token
    """
    user_id: int
    email: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify JWT token and extract user data
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")

        if user_id is None or email is None:
            return None

        token_data = TokenData(user_id=user_id, email=email)
        return token_data
    except JWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """
    Get current user from JWT token in request
    """
    token = credentials.credentials

    token_data = verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database to ensure they still exist
    user = session.get(User, token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify email matches the one in token
    if user.email != token_data.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token email doesn't match user email",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get current user ID from JWT token in request (for user_id verification)
    """
    token = credentials.credentials

    token_data = verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_data.user_id


def verify_user_id_match(request_user_id: int, token_user_id: int) -> bool:
    """
    Verify that the user_id in the request path matches the user_id in the JWT token
    This ensures that users can only access their own resources
    """
    return request_user_id == token_user_id


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate user with email and password
    This would typically involve password hashing comparison
    For this implementation, we'll assume password verification is handled elsewhere
    """
    # In a real implementation, you would:
    # 1. Find user by email
    # 2. Verify password using bcrypt or similar
    # 3. Return user if credentials match

    # Placeholder implementation - in real app, verify hashed password
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Find user by email
    user = session.query(User).filter(User.email == email).first()

    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None


def get_password_hash(password: str) -> str:
    """
    Generate password hash using bcrypt
    """
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def create_user(session: Session, email: str, password: str) -> User:
    """
    Create a new user with hashed password
    """
    hashed_password = get_password_hash(password)
    db_user = User(email=email, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# Dependency to be used in API routes
CurrentUser = Depends(get_current_user)
CurrentUserId = Depends(get_current_user_id)