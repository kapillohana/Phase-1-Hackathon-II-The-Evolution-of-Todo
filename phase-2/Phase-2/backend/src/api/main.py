"""
Main API endpoints for the Advanced Todo Application
Implements all required endpoints with advanced features and authentication
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Optional
from datetime import datetime, timedelta
import os
import json

from ..database.database import get_session
from ..auth.auth import CurrentUser, verify_user_id_match, get_current_user_id, get_current_user
from ..crud.crud import (
    create_task, get_task, get_tasks, get_tasks_count,
    update_task, delete_task, toggle_task_completion, calculate_next_due_date
)
from ..models.models import User, Task
from ..schemas.task_schemas import (
    TaskCreate, TaskUpdate, TaskPublic, TaskToggleComplete,
    TaskListQueryParams, TaskListResponse, PaginationInfo
)
from .auth import router as auth_router

# Create API router instance (not a full FastAPI app)
router = APIRouter()

# Include authentication routes under the main API router
# Note: auth routes are included separately in main.py

@router.post("/{user_id}/tasks", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_new_task(
    user_id: int,
    task_create: TaskCreate,
    token_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user
    """
    # Verify that the user_id in the path matches the user_id in the JWT token
    if not verify_user_id_match(user_id, token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Verify the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create the task
    db_task = create_task(session, user_id, task_create)

    # Convert to public model
    task_public = TaskPublic(
        id=db_task.id,
        user_id=db_task.user_id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
        priority=db_task.priority,
        tags=json.loads(db_task.tags) if db_task.tags else [],
        due_date=db_task.due_date,
        recurring=db_task.recurring,
        completed_at=db_task.completed_at,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at
    )

    return task_public


@router.get("/{user_id}/tasks", response_model=TaskListResponse)
def list_tasks(
    user_id: int,
    token_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
    search: Optional[str] = Query(None, description="Search keyword in title/description"),
    filter_status: Optional[str] = Query(None, description="Filter by completion status (completed, pending, all)"),
    filter_priority: Optional[str] = Query(None, description="Filter by priority (high, medium, low, all)"),
    filter_date: Optional[str] = Query(None, description="Filter by due date range (past, today, upcoming, overdue, all)"),
    sort: Optional[str] = Query(None, description="Sort field (due_date, priority, created_at, title, completed)"),
    ascending: Optional[bool] = Query(False, description="Sort direction (true for ascending, false for descending)"),
    page: int = Query(1, ge=1, description="Page number (default: 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (default: 20, max: 100)")
):
    """
    List all tasks for the specified user with optional filtering, searching, and sorting
    """
    # Verify that the user_id in the path matches the user_id in the JWT token
    if not verify_user_id_match(user_id, token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Verify the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Calculate pagination parameters
    skip = (page - 1) * page_size

    # Get tasks with filters
    db_tasks = get_tasks(
        session=session,
        user_id=user_id,
        search=search,
        filter_status=filter_status,
        filter_priority=filter_priority,
        filter_date=filter_date,
        sort=sort,
        ascending=ascending,
        skip=skip,
        limit=page_size
    )

    # Get total count for pagination
    total_count = get_tasks_count(
        session=session,
        user_id=user_id,
        search=search,
        filter_status=filter_status,
        filter_priority=filter_priority,
        filter_date=filter_date
    )

    # Convert database tasks to public models
    tasks_public = []
    for db_task in db_tasks:
        task_public = TaskPublic(
            id=db_task.id,
            user_id=db_task.user_id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            priority=db_task.priority,
            tags=json.loads(db_task.tags) if db_task.tags else [],
            due_date=db_task.due_date,
            recurring=db_task.recurring,
            completed_at=db_task.completed_at,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at
        )
        tasks_public.append(task_public)

    # Calculate pagination info
    total_pages = (total_count + page_size - 1) // page_size
    has_next = page < total_pages
    has_prev = page > 1

    pagination_info = PaginationInfo(
        page=page,
        page_size=page_size,
        total=total_count,
        total_pages=total_pages,
        has_next=has_next,
        has_prev=has_prev
    )

    # Prepare response
    response_data = {
        "tasks": tasks_public,
        "pagination": pagination_info
    }

    filters_applied = {}
    if search:
        filters_applied["search"] = search
    if filter_status:
        filters_applied["filter_status"] = filter_status
    if filter_priority:
        filters_applied["filter_priority"] = filter_priority
    if filter_date:
        filters_applied["filter_date"] = filter_date
    if sort:
        filters_applied["sort"] = sort
        filters_applied["ascending"] = ascending

    return TaskListResponse(
        success=True,
        data=response_data,
        filters_applied=filters_applied if filters_applied else None,
        message="Tasks retrieved successfully"
    )


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskPublic)
def get_single_task(
    user_id: int,
    task_id: int,
    token_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a single task by ID for the specified user
    """
    # Verify that the user_id in the path matches the user_id in the JWT token
    if not verify_user_id_match(user_id, token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Verify the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get the task
    db_task = get_task(session, task_id, user_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Convert to public model
    task_public = TaskPublic(
        id=db_task.id,
        user_id=db_task.user_id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
        priority=db_task.priority,
        tags=json.loads(db_task.tags) if db_task.tags else [],
        due_date=db_task.due_date,
        recurring=db_task.recurring,
        completed_at=db_task.completed_at,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at
    )

    return task_public


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskPublic)
def update_existing_task(
    user_id: int,
    task_id: int,
    task_update: TaskUpdate,
    token_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the specified user
    """
    # Verify that the user_id in the path matches the user_id in the JWT token
    if not verify_user_id_match(user_id, token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Verify the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update the task
    db_task = update_task(session, task_id, user_id, task_update)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Convert to public model
    task_public = TaskPublic(
        id=db_task.id,
        user_id=db_task.user_id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
        priority=db_task.priority,
        tags=json.loads(db_task.tags) if db_task.tags else [],
        due_date=db_task.due_date,
        recurring=db_task.recurring,
        completed_at=db_task.completed_at,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at
    )

    return task_public


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_200_OK)
def remove_task(
    user_id: int,
    task_id: int,
    token_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the specified user
    """
    # Verify that the user_id in the path matches the user_id in the JWT token
    if not verify_user_id_match(user_id, token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Verify the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete the task
    success = delete_task(session, task_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"success": True, "message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=dict)
def toggle_task_completion_status(
    user_id: int,
    task_id: int,
    task_toggle: TaskToggleComplete,
    token_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task
    If completed is provided in the request body, set to that value; otherwise toggle current status
    """
    # Verify that the user_id in the path matches the user_id in the JWT token
    if not verify_user_id_match(user_id, token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Verify the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Toggle task completion
    db_task = toggle_task_completion(session, task_id, user_id, task_toggle.completed)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    response_data = {
        "id": db_task.id,
        "completed": db_task.completed,
        "completed_at": db_task.completed_at
    }

    # If this was a recurring task and was completed, indicate that a new task was scheduled
    recurring_action = None
    if db_task.completed and db_task.recurring != 'none':
        recurring_action = f"New recurring task created based on {db_task.recurring} pattern"

    return {
        "success": True,
        "data": response_data,
        "message": "Task completion status updated",
        "recurring_action": recurring_action
    }