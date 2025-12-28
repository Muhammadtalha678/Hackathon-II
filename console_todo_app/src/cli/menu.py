"""
Menu interface for the Console Todo App.

This module contains the Menu class that provides the interactive
command-line interface for the todo application.
"""
from typing import Optional
from src.services.todo_service import TodoService


class Menu:
    """
    Provides the interactive menu interface for the Console Todo App.
    """

    def __init__(self, todo_service: TodoService):
        """
        Initialize the Menu with a TodoService.

        Args:
            todo_service: The TodoService to use for todo operations
        """
        self.todo_service = todo_service

    def display_menu(self):
        """
        Display the main menu options to the user.
        """
        print("\n=== Todo Manager ===")
        print("1. View all tasks")
        print("2. Add new task")
        print("3. Mark task as complete/incomplete")
        print("4. Update task")
        print("5. Delete task")
        print("6. Exit")

    def handle_add_todo(self):
        """
        Handle the add todo functionality.
        """
        try:
            title = input("Enter task title: ").strip()
            description = input("Enter description (optional): ").strip()

            if not title:
                print("Error: Title cannot be empty.")
                return

            todo = self.todo_service.add_todo(description if description else title, title)
            print(f"✓ Task created with ID: {todo.id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_view_todos(self):
        """
        Handle the view todos functionality.
        """
        todos = self.todo_service.get_all_todos()
        if not todos:
            print("No tasks yet. Add your first task!")
            return

        print("\n=== Your Tasks ===")
        print("\nID  Status  Title                          Created")
        print("------------------------------------------------------------")

        pending_count = 0
        completed_count = 0

        for todo in todos:
            status = "[x]" if todo.completed else "[ ]"
            # Format the title to fit in the column
            title_display = todo.title[:30] if len(todo.title) > 30 else todo.title
            title_display = title_display.ljust(30)  # Pad to 30 characters
            created_date = todo.created_at.strftime("%Y-%m-%d %H:%M")

            print(f"{todo.id[:3]:<3} {status}     {title_display} {created_date}")

            if todo.completed:
                completed_count += 1
            else:
                pending_count += 1

        total = len(todos)
        print(f"\nTotal: {total} tasks ({pending_count} pending, {completed_count} completed)")

    def handle_mark_complete(self):
        """
        Handle marking a todo as complete.
        """
        todos = self.todo_service.get_all_todos()
        if not todos:
            print("No tasks available to mark as complete.")
            return

        self.handle_view_todos()
        task_id = input("Enter task ID to toggle complete/incomplete: ").strip()

        # Check current status and toggle
        todo = self.todo_service.get_todo_by_id(task_id)
        if not todo:
            print(f"Error: Task with ID '{task_id}' not found.")
            return

        if todo.completed:
            self.todo_service.mark_incomplete(task_id)
            print(f"Task '{todo.title}' marked as incomplete.")
        else:
            self.todo_service.mark_complete(task_id)
            print(f"Task '{todo.title}' marked as complete.")

    def handle_update_todo(self):
        """
        Handle updating a todo's description.
        """
        todos = self.todo_service.get_all_todos()
        if not todos:
            print("No tasks available to update.")
            return

        self.handle_view_todos()
        task_id = input("Enter task ID to update: ").strip()

        # Get the current todo to show its current details
        current_todo = self.todo_service.get_todo_by_id(task_id)
        if not current_todo:
            print(f"Error: Task with ID '{task_id}' not found.")
            return

        print(f"Current title: {current_todo.title}")
        print(f"Current description: {current_todo.description}")

        new_title = input(f"Enter new title (or press Enter to keep '{current_todo.title}'): ").strip()
        new_description = input(f"Enter new description (or press Enter to keep current): ").strip()

        # Use existing values if user doesn't provide new ones
        if not new_title:
            new_title = current_todo.title
        if not new_description:
            new_description = current_todo.description

        try:
            if self.todo_service.update_todo(task_id, new_description, new_title):
                print("Task updated successfully.")
            else:
                print(f"Error: Task with ID '{task_id}' not found.")
        except ValueError as e:
            print(f"Error: {e}")

    def handle_delete_todo(self):
        """
        Handle deleting a todo.
        """
        todos = self.todo_service.get_all_todos()
        if not todos:
            print("No tasks available to delete.")
            return

        self.handle_view_todos()
        task_id = input("Enter task ID to delete: ").strip()

        # Get the todo to show its details before deletion
        todo = self.todo_service.get_todo_by_id(task_id)
        if not todo:
            print(f"Error: Task with ID '{task_id}' not found.")
            return

        confirm = input(f"Are you sure you want to delete '{todo.title}'? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            if self.todo_service.delete_todo(task_id):
                print(f"Task '{todo.title}' deleted successfully.")
            else:
                print(f"Error: Could not delete task with ID '{task_id}'.")
        else:
            print("Deletion cancelled.")

    def get_user_choice(self) -> str:
        """
        Get the user's menu choice.

        Returns:
            The user's choice as a string
        """
        return input("Enter your choice (1-6): ").strip()

    def handle_invalid_choice(self, choice: str):
        """
        Handle invalid menu choices.

        Args:
            choice: The invalid choice entered by the user
        """
        print(f"Invalid choice: '{choice}'. Please enter a number between 1 and 6.")