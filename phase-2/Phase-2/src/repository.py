from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Task


class TaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Task]:
        """Return all tasks"""
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by ID"""
        pass

    @abstractmethod
    def add(self, task: Task) -> Task:
        """Add a new task to the repository"""
        pass

    @abstractmethod
    def update(self, task_id: int, **updates) -> Optional[Task]:
        """Update a task by ID"""
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Delete a task by ID"""
        pass

    @abstractmethod
    def generate_id(self) -> int:
        """Generate next available ID"""
        pass


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1  # For ID generation

    def get_all(self) -> List[Task]:
        """Return all tasks"""
        return self._tasks.copy()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by ID"""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def add(self, task: Task) -> Task:
        """Add a new task to the repository"""
        self._tasks.append(task)
        return task

    def update(self, task_id: int, **updates) -> Optional[Task]:
        """Update a task by ID"""
        task = self.get_by_id(task_id)
        if task:
            for field, value in updates.items():
                if hasattr(task, field):
                    setattr(task, field, value)
            return task
        return None

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID"""
        task = self.get_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def generate_id(self) -> int:
        """Generate next available ID"""
        new_id = self._next_id
        self._next_id += 1
        return new_id