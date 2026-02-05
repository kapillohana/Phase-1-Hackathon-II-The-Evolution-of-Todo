"""
Pydantic schemas for Task-related API endpoints
Defines request/response models for task operations
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class PriorityEnum(str, Enum):
    """
    Enum for task priority levels
    """
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecurringEnum(str, Enum):
    """
    Enum for recurring task patterns
    """
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class TaskCreate(BaseModel):
    """
    Schema for creating new tasks
    """
    title: str = Field(..., min_length=1, max_length=255, description="Task title (required)")
    description: Optional[str] = Field(None, max_length=1000, description="Task description (optional)")
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM, description="Task priority (high/medium/low)")
    tags: Optional[List[str]] = Field(None, max_items=10, description="Task tags (max 10 tags)")
    due_date: Optional[datetime] = Field(None, description="Task due date (ISO 8601 format)")
    recurring: RecurringEnum = Field(default=RecurringEnum.NONE, description="Task recurrence pattern")

    @validator('tags')
    def validate_tags(cls, v):
        if v is None:
            return v
        # Validate each tag length
        for tag in v:
            if len(tag) > 50:
                raise ValueError(f'Tag "{tag}" exceeds 50 character limit')
        return v

    @validator('due_date')
    def validate_due_date(cls, v):
        if v is not None and v < datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return v

    class Config:
        schema_extra = {
            "example": {
                "title": "Complete project proposal",
                "description": "Finish writing the project proposal document",
                "priority": "high",
                "tags": ["work", "important"],
                "due_date": "2026-12-31T23:59:59Z",
                "recurring": "none"
            }
        }


class TaskUpdate(BaseModel):
    """
    Schema for partially updating tasks
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[PriorityEnum] = None
    tags: Optional[List[str]] = Field(None, max_items=10)
    due_date: Optional[datetime] = None
    recurring: Optional[RecurringEnum] = None
    completed: Optional[bool] = None

    @validator('tags')
    def validate_tags(cls, v):
        if v is None:
            return v
        # Validate each tag length
        for tag in v:
            if len(tag) > 50:
                raise ValueError(f'Tag "{tag}" exceeds 50 character limit')
        return v

    @validator('due_date')
    def validate_due_date(cls, v):
        if v is not None and v < datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return v

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated project proposal",
                "priority": "medium",
                "completed": True
            }
        }


class TaskPublic(BaseModel):
    """
    Public schema for task responses
    """
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: PriorityEnum
    tags: Optional[List[str]]
    due_date: Optional[datetime]
    recurring: RecurringEnum
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "user_id": 456,
                "title": "Complete project proposal",
                "description": "Finish writing the project proposal document",
                "completed": False,
                "priority": "high",
                "tags": ["work", "important"],
                "due_date": "2026-12-31T23:59:59Z",
                "recurring": "none",
                "completed_at": None,
                "created_at": "2026-01-11T10:00:00Z",
                "updated_at": "2026-01-11T10:00:00Z"
            }
        }


class TaskToggleComplete(BaseModel):
    """
    Schema for toggling task completion status
    """
    completed: Optional[bool] = Field(None, description="New completion status. If omitted, toggles current status")

    class Config:
        schema_extra = {
            "example": {
                "completed": True
            }
        }


class TaskListQueryParams(BaseModel):
    """
    Query parameters for listing tasks
    """
    search: Optional[str] = Field(None, description="Search keyword in title/description")
    filter_status: Optional[str] = Field(None, description="Filter by completion status (completed, pending, all)")
    filter_priority: Optional[str] = Field(None, description="Filter by priority (high, medium, low, all)")
    filter_date: Optional[str] = Field(None, description="Filter by due date range (past, today, upcoming, overdue, all)")
    sort: Optional[str] = Field(None, description="Sort field (due_date, priority, created_at, title, completed)")
    ascending: Optional[bool] = Field(False, description="Sort direction (true for ascending, false for descending)")
    page: Optional[int] = Field(1, ge=1, description="Page number (default: 1)")
    page_size: Optional[int] = Field(20, ge=1, le=100, description="Items per page (default: 20, max: 100)")

    class Config:
        schema_extra = {
            "example": {
                "search": "project",
                "filter_status": "pending",
                "filter_priority": "high",
                "sort": "due_date",
                "ascending": False,
                "page": 1,
                "page_size": 20
            }
        }


class PaginationInfo(BaseModel):
    """
    Pagination information for task list responses
    """
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TaskToggleComplete(BaseModel):
    """
    Schema for toggling task completion status
    """
    completed: Optional[bool] = Field(None, description="New completion status. If omitted, toggles current status")

    class Config:
        schema_extra = {
            "example": {
                "completed": True
            }
        }


class TaskListResponse(BaseModel):
    """
    Response schema for task list endpoint
    """
    success: bool
    data: Dict[str, Any]
    filters_applied: Optional[Dict[str, Any]] = None
    message: str

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "tasks": [
                        {
                            "id": 123,
                            "user_id": 456,
                            "title": "Complete project proposal",
                            "description": "Finish writing the project proposal document",
                            "completed": False,
                            "priority": "high",
                            "tags": ["work", "important"],
                            "due_date": "2026-12-31T23:59:59Z",
                            "recurring": "none",
                            "completed_at": None,
                            "created_at": "2026-01-11T10:00:00Z",
                            "updated_at": "2026-01-11T10:00:00Z"
                        }
                    ],
                    "pagination": {
                        "page": 1,
                        "page_size": 20,
                        "total": 150,
                        "total_pages": 8,
                        "has_next": True,
                        "has_prev": False
                    }
                },
                "filters_applied": {
                    "search": "project",
                    "filter_status": "pending",
                    "filter_priority": "high",
                    "sort": "due_date"
                },
                "message": "Tasks retrieved successfully"
            }
        }