"""
TodoService class providing business logic for todo operations.

This module contains the TodoService class that manages all todo operations
including adding, retrieving, updating, and deleting todo items.
"""
from typing import List, Optional
from src.models.todo_item import TodoItem


class TodoService:
    """
    Provides business logic for todo operations.
    """

    def __init__(self):
        """
        Initialize the TodoService with an empty list of todo items.
        """
        self.todos: List[TodoItem] = []
        self.next_id: int = 1

    def add_todo(self, description: str, title: str = "") -> TodoItem:
        """
        Add a new todo item to the list.

        Args:
            description: The description of the new todo item
            title: Optional title for the new todo item

        Returns:
            The newly created TodoItem

        Raises:
            ValueError: If the description is empty or exceeds 500 characters
        """
        # Validate description before creating the TodoItem
        self.validate_description(description)

        # Create a new TodoItem with a sequential ID
        new_id = str(self.next_id)
        todo_item = TodoItem(description=description, title=title, todo_id=new_id)
        self.todos.append(todo_item)
        self.next_id += 1
        return todo_item

    def get_all_todos(self) -> List[TodoItem]:
        """
        Get all todo items in the list.

        Returns:
            A list of all TodoItems
        """
        return self.todos.copy()  # Return a copy to prevent external modification

    def get_todo_by_id(self, todo_id: str) -> Optional[TodoItem]:
        """
        Get a specific todo item by its ID.

        Args:
            todo_id: The ID of the todo item to retrieve

        Returns:
            The TodoItem if found, None otherwise
        """
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo(self, todo_id: str, new_description: str, new_title: str = "") -> bool:
        """
        Update the description and title of an existing todo item.

        Args:
            todo_id: The ID of the todo item to update
            new_description: The new description for the todo item
            new_title: The new title for the todo item (optional)

        Returns:
            True if the update was successful, False if the todo item was not found

        Raises:
            ValueError: If the new description is empty or exceeds 500 characters
        """
        # Validate new description
        if not new_description or not new_description.strip():
            raise ValueError("Description cannot be empty or whitespace only")

        if len(new_description) > 500:
            raise ValueError("Description must be under 500 characters")

        # Find and update the todo item
        for todo in self.todos:
            if todo.id == todo_id:
                todo.description = new_description.strip()
                if new_title.strip():
                    todo.title = new_title.strip()
                return True
        return False

    def validate_description(self, description: str) -> None:
        """
        Validate a todo description.

        Args:
            description: The description to validate

        Raises:
            ValueError: If the description is empty, whitespace only, or too long
        """
        if not description or not description.strip():
            raise ValueError("Description cannot be empty or whitespace only")

        if len(description) > 500:
            raise ValueError("Description must be under 500 characters")

    def mark_complete(self, todo_id: str) -> bool:
        """
        Mark a todo item as complete.

        Args:
            todo_id: The ID of the todo item to mark as complete

        Returns:
            True if the operation was successful, False if the todo item was not found
        """
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo.completed = True
            return True
        return False

    def mark_incomplete(self, todo_id: str) -> bool:
        """
        Mark a todo item as incomplete.

        Args:
            todo_id: The ID of the todo item to mark as incomplete

        Returns:
            True if the operation was successful, False if the todo item was not found
        """
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo.completed = False
            return True
        return False

    def delete_todo(self, todo_id: str) -> bool:
        """
        Delete a todo item from the list.

        Args:
            todo_id: The ID of the todo item to delete

        Returns:
            True if the deletion was successful, False if the todo item was not found
        """
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                return True
        return False