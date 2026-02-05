"""
Authentication API endpoints for the Advanced Todo Application
Implements user registration, login, logout, and profile endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from pydantic import BaseModel
from typing import Optional
import os
from datetime import timedelta

from ..database.database import get_session
from ..auth.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_user as auth_create_user
)
from ..models.models import User
from ..schemas.user_schemas import UserCreate, UserLogin, UserPublic, TokenResponse

# Create a new router for authentication endpoints
router = APIRouter(prefix="/auth", tags=["authentication"])

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=TokenResponse)
def register_user(
    user_create: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user account
    """
    # Check if user already exists
    existing_user = session.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    try:
        db_user = auth_create_user(session, user_create.email, user_create.password)

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": db_user.id, "email": db_user.email},
            expires_delta=access_token_expires
        )

        return TokenResponse(access_token=access_token, token_type="bearer")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
def login_user(
    user_login: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return access token
    """
    user = authenticate_user(session, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/logout")
def logout_user():
    """
    Logout user (client-side token removal is sufficient)
    """
    # For JWT tokens, logout is typically handled client-side by removing the token
    # Server-side session management would require additional implementation
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserPublic)
def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's profile information
    """
    # Return user information (excluding sensitive data like hashed password)
    return UserPublic(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )


@router.post("/refresh")
def refresh_token():
    """
    Refresh access token (placeholder - would require refresh token implementation)
    """
    # This would require storing refresh tokens and implementing refresh logic
    # For now, returning a 501 Not Implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not implemented in this version"
    )