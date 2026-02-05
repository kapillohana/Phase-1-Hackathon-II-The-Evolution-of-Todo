"""
CRUD operations for the Advanced Todo Application
Handles all database operations for users and tasks with advanced features
"""
from typing import List, Optional
from sqlmodel import Session, select, func
from datetime import datetime, timedelta
from ..models.models import User, Task, TaskCreate, TaskUpdate
from ..schemas.task_schemas import PriorityEnum, RecurringEnum
import json


def create_task(session: Session, user_id: int, task_create: TaskCreate) -> Task:
    """
    Create a new task for the specified user
    """
    # Convert tags list to JSON string for storage
    tags_json = None
    if task_create.tags:
        tags_json = json.dumps(task_create.tags)

    db_task = Task(
        user_id=user_id,
        title=task_create.title,
        description=task_create.description,
        priority=task_create.priority.value,
        tags=tags_json,
        due_date=task_create.due_date,
        recurring=task_create.recurring.value,
        completed=task_create.completed if hasattr(task_create, 'completed') else False
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


def get_task(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Get a specific task by ID for the specified user
    Ensures user isolation by checking user_id
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def get_tasks(
    session: Session,
    user_id: int,
    search: Optional[str] = None,
    filter_status: Optional[str] = None,
    filter_priority: Optional[str] = None,
    filter_date: Optional[str] = None,
    sort: Optional[str] = None,
    ascending: bool = False,
    skip: int = 0,
    limit: int = 20
) -> List[Task]:
    """
    Get all tasks for the specified user with optional filtering, searching, and sorting
    """
    statement = select(Task).where(Task.user_id == user_id)

    # Apply search filter
    if search:
        search_lower = f"%{search.lower()}%"
        statement = statement.where(
            (func.lower(Task.title).contains(search_lower)) |
            (func.lower(Task.description).contains(search_lower))
        )

    # Apply status filter
    if filter_status and filter_status.lower() != 'all':
        if filter_status.lower() == 'completed':
            statement = statement.where(Task.completed == True)
        elif filter_status.lower() == 'pending':
            statement = statement.where(Task.completed == False)

    # Apply priority filter
    if filter_priority and filter_priority.lower() != 'all':
        statement = statement.where(Task.priority == filter_priority.lower())

    # Apply date filter
    if filter_date and filter_date.lower() != 'all':
        now = datetime.utcnow()
        if filter_date.lower() == 'past':
            statement = statement.where(Task.due_date < now)
        elif filter_date.lower() == 'today':
            # Filter for tasks due today
            statement = statement.where(
                func.date(Task.due_date) == func.date(now)
            )
        elif filter_date.lower() == 'upcoming':
            statement = statement.where(Task.due_date > now)
        elif filter_date.lower() == 'overdue':
            statement = statement.where(
                Task.due_date < now,
                Task.completed == False
            )

    # Apply sorting
    if sort:
        if sort == 'due_date':
            order_field = Task.due_date
        elif sort == 'priority':
            order_field = Task.priority
        elif sort == 'created_at':
            order_field = Task.created_at
        elif sort == 'title':
            order_field = Task.title
        elif sort == 'completed':
            order_field = Task.completed
        else:
            order_field = Task.created_at  # Default to created_at

        if ascending:
            statement = statement.order_by(order_field.asc())
        else:
            statement = statement.order_by(order_field.desc())
    else:
        # Default sorting by creation date (newest first)
        statement = statement.order_by(Task.created_at.desc())

    # Apply pagination
    statement = statement.offset(skip).limit(limit)

    tasks = session.exec(statement).all()
    return tasks


def get_tasks_count(
    session: Session,
    user_id: int,
    search: Optional[str] = None,
    filter_status: Optional[str] = None,
    filter_priority: Optional[str] = None,
    filter_date: Optional[str] = None
) -> int:
    """
    Get count of tasks for pagination
    """
    statement = select(func.count(Task.id)).where(Task.user_id == user_id)

    # Apply the same filters as get_tasks
    if search:
        search_lower = f"%{search.lower()}%"
        statement = statement.where(
            (func.lower(Task.title).contains(search_lower)) |
            (func.lower(Task.description).contains(search_lower))
        )

    if filter_status and filter_status.lower() != 'all':
        if filter_status.lower() == 'completed':
            statement = statement.where(Task.completed == True)
        elif filter_status.lower() == 'pending':
            statement = statement.where(Task.completed == False)

    if filter_priority and filter_priority.lower() != 'all':
        statement = statement.where(Task.priority == filter_priority.lower())

    if filter_date and filter_date.lower() != 'all':
        now = datetime.utcnow()
        if filter_date.lower() == 'past':
            statement = statement.where(Task.due_date < now)
        elif filter_date.lower() == 'today':
            statement = statement.where(
                func.date(Task.due_date) == func.date(now)
            )
        elif filter_date.lower() == 'upcoming':
            statement = statement.where(Task.due_date > now)
        elif filter_date.lower() == 'overdue':
            statement = statement.where(
                Task.due_date < now,
                Task.completed == False
            )

    count = session.exec(statement).one()
    return count


def update_task(session: Session, task_id: int, user_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """
    Update a specific task for the specified user
    """
    db_task = get_task(session, task_id, user_id)
    if not db_task:
        return None

    # Update fields if provided in the update object
    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    if task_update.completed is not None:
        db_task.completed = task_update.completed
        if task_update.completed:
            # Set completed_at when marking as complete
            db_task.completed_at = datetime.utcnow()
        else:
            # Clear completed_at when marking as incomplete
            db_task.completed_at = None
    if task_update.priority is not None:
        db_task.priority = task_update.priority.value
    if task_update.tags is not None:
        # Convert tags list to JSON string
        db_task.tags = json.dumps(task_update.tags) if task_update.tags else None
    if task_update.due_date is not None:
        db_task.due_date = task_update.due_date
    if task_update.recurring is not None:
        db_task.recurring = task_update.recurring.value

    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    """
    Delete a specific task for the specified user
    """
    db_task = get_task(session, task_id, user_id)
    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: int, user_id: int, completed: Optional[bool] = None) -> Optional[Task]:
    """
    Toggle the completion status of a task
    If completed is provided, set to that value; otherwise toggle current status
    """
    db_task = get_task(session, task_id, user_id)
    if not db_task:
        return None

    # Determine new completion status
    if completed is not None:
        db_task.completed = completed
    else:
        # Toggle current status
        db_task.completed = not db_task.completed

    # Set completed_at timestamp if completing task, clear if uncompleting
    if db_task.completed:
        db_task.completed_at = datetime.utcnow()
    else:
        db_task.completed_at = None

    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    # Check if this is a recurring task and handle auto-rescheduling
    if db_task.completed and db_task.recurring != 'none':
        schedule_next_recurring_task(session, db_task)

    return db_task


def schedule_next_recurring_task(session: Session, completed_task: Task) -> Optional[Task]:
    """
    Create a new task instance based on the recurring pattern of a completed task
    """
    if completed_task.recurring == 'none':
        return None

    # Calculate next due date based on recurrence pattern
    next_due_date = calculate_next_due_date(completed_task.due_date, completed_task.recurring)

    # Convert tags JSON back to list
    tags_list = json.loads(completed_task.tags) if completed_task.tags else []

    # Create new task with same properties as the completed one
    new_task = Task(
        user_id=completed_task.user_id,
        title=completed_task.title,
        description=completed_task.description,
        priority=completed_task.priority,
        tags=completed_task.tags,
        due_date=next_due_date,
        recurring=completed_task.recurring,  # Keep the same recurrence pattern
        completed=False,  # New task starts as incomplete
        completed_at=None
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


def calculate_next_due_date(current_due_date: Optional[datetime], recurring_pattern: str) -> Optional[datetime]:
    """
    Calculate the next due date based on the current due date and recurrence pattern
    """
    if not current_due_date:
        return None

    if recurring_pattern == 'daily':
        return current_due_date + timedelta(days=1)
    elif recurring_pattern == 'weekly':
        return current_due_date + timedelta(weeks=1)
    elif recurring_pattern == 'monthly':
        # For monthly, add approximately one month (30 days)
        # In a production system, you might want to handle months with different numbers of days
        return current_due_date + timedelta(days=30)
    else:
        return None


def get_user(session: Session, user_id: int) -> Optional[User]:
    """
    Get a user by ID
    """
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Get a user by email
    """
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def create_user(session: Session, email: str, hashed_password: str) -> User:
    """
    Create a new user
    """
    db_user = User(email=email, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
