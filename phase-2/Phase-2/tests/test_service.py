import unittest
from unittest.mock import Mock
from src.models import Task
from src.service import TodoService
from src.repository import TaskRepository


class TestTodoService(unittest.TestCase):
    def setUp(self):
        # Create a mock repository for testing
        self.mock_repository = Mock(spec=TaskRepository)
        self.service = TodoService(self.mock_repository)

    def test_add_task_success(self):
        """Test adding a task successfully"""
        # Arrange
        self.mock_repository.generate_id.return_value = 1
        expected_task = Task(id=1, title="Test Task", completed=False)
        self.mock_repository.add.return_value = expected_task

        # Act
        result = self.service.add_task("Test Task")

        # Assert
        self.assertEqual(result, expected_task)
        self.mock_repository.generate_id.assert_called_once()
        self.mock_repository.add.assert_called_once_with(expected_task)

    def test_add_task_with_description(self):
        """Test adding a task with description"""
        # Arrange
        self.mock_repository.generate_id.return_value = 1
        expected_task = Task(id=1, title="Test Task", description="Test Description", completed=False)
        self.mock_repository.add.return_value = expected_task

        # Act
        result = self.service.add_task("Test Task", "Test Description")

        # Assert
        self.assertEqual(result, expected_task)
        self.mock_repository.add.assert_called_once_with(expected_task)

    def test_add_task_empty_title_error(self):
        """Test that adding a task with empty title raises ValueError"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.service.add_task("")
        self.assertEqual(str(context.exception), "Title cannot be empty")

        with self.assertRaises(ValueError) as context:
            self.service.add_task("   ")  # whitespace only
        self.assertEqual(str(context.exception), "Title cannot be empty")

    def test_get_all_tasks(self):
        """Test getting all tasks"""
        # Arrange
        expected_tasks = [
            Task(id=1, title="Task 1", completed=False),
            Task(id=2, title="Task 2", completed=True)
        ]
        self.mock_repository.get_all.return_value = expected_tasks

        # Act
        result = self.service.get_all_tasks()

        # Assert
        self.assertEqual(result, expected_tasks)
        self.mock_repository.get_all.assert_called_once()

    def test_update_task_success(self):
        """Test updating a task successfully"""
        # Arrange
        existing_task = Task(id=1, title="Old Title", description="Old Description", completed=False)
        self.mock_repository.get_by_id.return_value = existing_task
        updated_task = Task(id=1, title="New Title", description="New Description", completed=False)
        self.mock_repository.update.return_value = updated_task

        # Act
        result = self.service.update_task(1, "New Title", "New Description")

        # Assert
        self.assertEqual(result, updated_task)
        self.mock_repository.get_by_id.assert_called_once_with(1)
        self.mock_repository.update.assert_called_once_with(1, title="New Title", description="New Description")

    def test_update_task_partial(self):
        """Test updating only title or description"""
        # Arrange
        existing_task = Task(id=1, title="Old Title", completed=False)
        self.mock_repository.get_by_id.return_value = existing_task
        updated_task = Task(id=1, title="New Title", completed=False)
        self.mock_repository.update.return_value = updated_task

        # Act
        result = self.service.update_task(1, title="New Title")

        # Assert
        self.assertEqual(result, updated_task)
        self.mock_repository.update.assert_called_once_with(1, title="New Title")

    def test_update_task_empty_title_error(self):
        """Test that updating a task with empty title raises ValueError"""
        # Arrange
        existing_task = Task(id=1, title="Old Title", completed=False)
        self.mock_repository.get_by_id.return_value = existing_task

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.service.update_task(1, "")
        self.assertEqual(str(context.exception), "Title cannot be empty")

        with self.assertRaises(ValueError) as context:
            self.service.update_task(1, "   ")  # whitespace only
        self.assertEqual(str(context.exception), "Title cannot be empty")

    def test_update_task_nonexistent_error(self):
        """Test that updating a non-existent task raises ValueError"""
        # Arrange
        self.mock_repository.get_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.service.update_task(999, "New Title")
        self.assertEqual(str(context.exception), "Task with ID 999 does not exist")

    def test_complete_task_success(self):
        """Test completing a task successfully"""
        # Arrange
        existing_task = Task(id=1, title="Test Task", completed=False)
        self.mock_repository.get_by_id.return_value = existing_task
        completed_task = Task(id=1, title="Test Task", completed=True)
        self.mock_repository.update.return_value = completed_task

        # Act
        result = self.service.complete_task(1)

        # Assert
        self.assertTrue(result)
        self.mock_repository.get_by_id.assert_called_once_with(1)
        self.mock_repository.update.assert_called_once_with(1, completed=True)

    def test_complete_task_nonexistent_error(self):
        """Test that completing a non-existent task raises ValueError"""
        # Arrange
        self.mock_repository.get_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.service.complete_task(999)
        self.assertEqual(str(context.exception), "Task with ID 999 does not exist")

    def test_delete_task_success(self):
        """Test deleting a task successfully"""
        # Arrange
        existing_task = Task(id=1, title="Test Task", completed=False)
        self.mock_repository.get_by_id.return_value = existing_task
        self.mock_repository.delete.return_value = True

        # Act
        result = self.service.delete_task(1)

        # Assert
        self.assertTrue(result)
        self.mock_repository.get_by_id.assert_called_once_with(1)
        self.mock_repository.delete.assert_called_once_with(1)

    def test_delete_task_nonexistent_error(self):
        """Test that deleting a non-existent task raises ValueError"""
        # Arrange
        self.mock_repository.get_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.service.delete_task(999)
        self.assertEqual(str(context.exception), "Task with ID 999 does not exist")


if __name__ == "__main__":
    unittest.main()