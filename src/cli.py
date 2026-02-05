import sys
from typing import Optional
from .service import TodoService
from .repository import InMemoryTaskRepository


class TodoCLI:
    def __init__(self, service: TodoService):
        """
        CLI receives service via dependency injection.
        This ensures the CLI only handles presentation logic while business logic
        remains in the service layer.
        """
        self.service = service

    @classmethod
    def create_default(cls):
        """
        Factory method to create a CLI instance with default dependencies.
        This is the main entry point that wires up all components.
        """
        repository = InMemoryTaskRepository()
        service = TodoService(repository)
        return cls(service)

    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("           📝 TODO CLI APPLICATION 📝")
        print("="*60)
        print("Welcome to your personal task manager!")
        print("Choose an option from the menu below:")
        print()
        print("1. ➕ Add New Task")
        print("2. 📋 View All Tasks")
        print("3. ✏️  Update Task")
        print("4. ✅ Mark Task as Complete")
        print("5. 🗑️  Delete Task")
        print("6. 🚪 Exit Application")
        print()
        print("="*60)

    def get_user_choice(self):
        """Get and validate user choice"""
        try:
            choice = input("Enter your choice (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                return None
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)
        except EOFError:
            print("\n\nGoodbye!")
            sys.exit(0)

    def run_interactive(self):
        """Main interactive loop"""
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice is None:
                continue

            if choice == 1:
                self.add_task_interactive()
            elif choice == 2:
                self.view_tasks_interactive()
            elif choice == 3:
                self.update_task_interactive()
            elif choice == 4:
                self.complete_task_interactive()
            elif choice == 5:
                self.delete_task_interactive()
            elif choice == 6:
                print("\n👋 Thank you for using the Todo CLI Application! Goodbye!")
                break

    def add_task_interactive(self):
        """Interactive method to add a task"""
        print("\n" + "-"*40)
        print("➕ ADD NEW TASK")
        print("-"*40)
        try:
            title = input("📝 Enter task title: ").strip()
            if not title:
                print("❌ Title cannot be empty!")
                return

            description = input("📋 Enter task description (optional, press Enter to skip): ").strip()
            if not description:  # If description is empty, set to None
                description = None

            task = self.service.add_task(title, description)
            print(f"✅ Success! Task #{task.id} created: {task.title}")
            print("-"*40)
        except ValueError as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except EOFError:
            print("\nOperation cancelled.")

    def view_tasks_interactive(self):
        """Interactive method to view all tasks"""
        print("\n" + "-"*50)
        print("📋 ALL TASKS")
        print("-"*50)
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("📭 No tasks found. Add some tasks to get started!")
            return

        # Count completed and pending tasks
        completed_count = sum(1 for task in tasks if task.completed)
        pending_count = len(tasks) - completed_count

        for task in tasks:
            status = "✅" if task.completed else "⏳"
            print(f"{task.id}. {status} {task.title}")
            if task.description:
                print(f"   📝 Description: {task.description}")

        print(f"\n📊 Summary: {pending_count} pending, {completed_count} completed out of {len(tasks)} total tasks")
        print("-"*50)

    def update_task_interactive(self):
        """Interactive method to update a task"""
        print("\n" + "-"*40)
        print("✏️  UPDATE TASK")
        print("-"*40)
        try:
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("📭 No tasks available to update.")
                return

            print("📋 Current tasks:")
            for task in tasks:
                status = "✅" if task.completed else "⏳"
                print(f"  {task.id}. {status} {task.title}")

            task_id = input("\n🔢 Enter task ID to update: ").strip()
            if not task_id.isdigit():
                print("❌ Invalid task ID. Please enter a number.")
                return

            task_id = int(task_id)

            # Check if task exists first
            task = self.service.get_all_tasks()
            target_task = None
            for t in task:
                if t.id == task_id:
                    target_task = t
                    break

            if not target_task:
                print(f"❌ No task found with ID {task_id}.")
                return

            print(f"📋 Selected task: {target_task.id}. {'✅' if target_task.completed else '⏳'} {target_task.title}")

            # Show current values and allow updates
            new_title = input(f"📝 Enter new title (current: '{target_task.title}', press Enter to keep current): ").strip()
            new_description = input(f"📋 Enter new description (current: '{target_task.description or 'None'}', press Enter to keep current): ").strip()

            # Use current values if user doesn't provide new ones
            title_update = new_title if new_title else None
            description_update = new_description if new_description else None

            # If user enters an empty string for description, we want to set it to None
            if new_description == "":
                description_update = None

            # Update task (only if there are changes)
            if title_update is not None or description_update is not None:
                task = self.service.update_task(task_id, title_update, description_update)
                print(f"✅ Success! Task #{task.id} updated: {task.title}")
            else:
                print("ℹ️  No changes made to the task.")
            print("-"*40)

        except ValueError as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except EOFError:
            print("\nOperation cancelled.")

    def complete_task_interactive(self):
        """Interactive method to complete a task"""
        print("\n" + "-"*40)
        print("✅ COMPLETE TASK")
        print("-"*40)
        try:
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("📭 No tasks available to complete.")
                return

            print("📋 Current tasks:")
            incomplete_tasks = [task for task in tasks if not task.completed]
            if not incomplete_tasks:
                print("🎉 All tasks are already completed!")
                return

            for task in incomplete_tasks:
                print(f"  {task.id}. ⏳ {task.title}")

            task_id = input(f"\n🔢 Enter task ID to mark as complete: ").strip()
            if not task_id.isdigit():
                print("❌ Invalid task ID. Please enter a number.")
                return

            task_id = int(task_id)
            self.service.complete_task(task_id)
            print(f"✅ Success! Task #{task_id} marked as complete.")

        except ValueError as e:
            print(f"✗ Error: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except EOFError:
            print("\nOperation cancelled.")

    def delete_task_interactive(self):
        """Interactive method to delete a task"""
        print("\n" + "-"*40)
        print("🗑️  DELETE TASK")
        print("-"*40)
        try:
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("📭 No tasks available to delete.")
                return

            print("📋 Current tasks:")
            for task in tasks:
                status = "✅" if task.completed else "⏳"
                print(f"  {task.id}. {status} {task.title}")

            task_id = input("\n🔢 Enter task ID to delete: ").strip()
            if not task_id.isdigit():
                print("❌ Invalid task ID. Please enter a number.")
                return

            task_id = int(task_id)
            self.service.delete_task(task_id)
            print(f"🗑️  Task #{task_id} deleted.")
            print("-"*40)

        except ValueError as e:
            print(f"✗ Error: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except EOFError:
            print("\nOperation cancelled.")

    def run(self, args=None):
        """Main entry point - run interactive mode if no arguments provided"""
        if args is not None:
            # For backward compatibility, though we're focusing on interactive mode
            pass

        # Run the interactive menu
        self.run_interactive()


def main():
    """Main entry point for the application"""
    cli = TodoCLI.create_default()
    cli.run()


if __name__ == "__main__":
    main()