"""
Database models for the Advanced Todo Application
Using SQLModel for ORM with advanced task features
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import json
from pydantic import BaseModel


class User(SQLModel, table=True):
    """
    User model representing registered users of the application
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class TaskBase(SQLModel):
    """
    Base model for task fields shared across different task operations
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", max_length=20)  # "high", "medium", "low"
    tags: Optional[str] = Field(default=None)  # JSON string for tags array
    due_date: Optional[datetime] = Field(default=None)
    recurring: str = Field(default="none", max_length=20)  # "none", "daily", "weekly", "monthly"
    completed_at: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """
    Task model representing user tasks with advanced features
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """
    Model for creating new tasks
    """
    title: str
    priority: str = "medium"
    recurring: str = "none"


class TaskUpdate(SQLModel):
    """
    Model for updating existing tasks (all fields optional for partial updates)
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None  # JSON string for tags array
    due_date: Optional[datetime] = None
    recurring: Optional[str] = None
    completed_at: Optional[datetime] = None


class TaskPublic(TaskBase):
    """
    Public model for task responses (includes IDs and timestamps)
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None


class UserPublic(SQLModel):
    """
    Public model for user responses (excludes sensitive data)
    """
    id: int
    email: str
    created_at: datetime
    updated_at: datetime