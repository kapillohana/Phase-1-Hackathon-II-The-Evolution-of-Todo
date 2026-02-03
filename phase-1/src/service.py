from typing import List, Optional
from .models import Task
from .repository import TaskRepository


class TodoService:
    def __init__(self, repository: TaskRepository):
        """
        Service layer receives repository via dependency injection.
        This allows for easy testing and future replacement of storage implementations.
        """
        self._repository = repository

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task with validation"""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        new_id = self._repository.generate_id()
        task = Task(id=new_id, title=title.strip(), description=description, completed=False)
        return self._repository.add(task)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self._repository.get_all()

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Update task with validation"""
        task = self._repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} does not exist")

        updates = {}
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            updates['title'] = title.strip()
        if description is not None:
            updates['description'] = description

        return self._repository.update(task_id, **updates)

    def complete_task(self, task_id: int) -> bool:
        """Mark task as completed"""
        task = self._repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} does not exist")

        result = self._repository.update(task_id, completed=True)
        return result is not None

    def delete_task(self, task_id: int) -> bool:
        """Delete task with validation"""
        if not self._repository.get_by_id(task_id):
            raise ValueError(f"Task with ID {task_id} does not exist")

        return self._repository.delete(task_id)