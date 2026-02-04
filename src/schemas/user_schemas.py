"""
Pydantic schemas for User-related API endpoints
Defines request/response models for user authentication and management
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import re


class UserCreate(BaseModel):
    """
    Schema for creating new users
    """
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")

    @validator('email')
    def validate_email(cls, v):
        # Basic email validation regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v.lower()

    @validator('password')
    def validate_password(cls, v):
        # Password must have at least one uppercase, lowercase, digit, and special character
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        }


class UserLogin(BaseModel):
    """
    Schema for user login
    """
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    @validator('email')
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v.lower()

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        }


class UserPublic(BaseModel):
    """
    Public schema for user responses (excludes sensitive data)
    """
    id: int
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "email": "user@example.com",
                "created_at": "2026-01-11T10:00:00Z",
                "updated_at": "2026-01-11T10:00:00Z"
            }
        }


class TokenResponse(BaseModel):
    """
    Schema for JWT token responses
    """
    access_token: str
    token_type: str = "bearer"
    expires_in: int

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 604800  # 7 days in seconds
            }
        }


class UserProfile(BaseModel):
    """
    Schema for user profile information
    """
    id: int
    email: str
    created_at: datetime
    updated_at: datetime
    task_count: int  # Number of tasks owned by the user

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "email": "user@example.com",
                "created_at": "2026-01-11T10:00:00Z",
                "updated_at": "2026-01-11T10:00:00Z",
                "task_count": 15
            }
        }