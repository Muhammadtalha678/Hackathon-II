"""
TodoItem model representing a single todo item.

This module contains the TodoItem class that represents a single todo item
with attributes like id, description, completion status, and creation timestamp.
"""
from datetime import datetime
from typing import Optional


class TodoItem:
    """
    Represents a single todo item with id, description, completion status, and creation timestamp.
    """

    def __init__(self, description: str, title: str = "", todo_id: Optional[str] = None, completed: bool = False):
        """
        Initialize a TodoItem.

        Args:
            description: The description of the todo item
            title: The title of the todo item (optional, defaults to description if empty)
            todo_id: Optional ID for the todo item. If not provided, will be set later
            completed: Whether the todo item is completed (default: False)
        """
        if not description or not description.strip():
            raise ValueError("Description cannot be empty or whitespace only")

        if len(description) > 500:
            raise ValueError("Description must be under 500 characters")

        self.id = todo_id
        self.description = description.strip()
        self.title = title.strip() if title.strip() else description.strip()
        self.completed = completed
        self.created_at = datetime.now()

    def __str__(self) -> str:
        """
        String representation of the TodoItem.

        Returns:
            A string representation showing the todo status and description
        """
        status = "x" if self.completed else " "
        return f"[{status}] {self.id}: {self.title}"

    def __repr__(self) -> str:
        """
        Developer-friendly representation of the TodoItem.

        Returns:
            A detailed string representation of the TodoItem
        """
        return (f"TodoItem(id={self.id!r}, title={self.title!r}, description={self.description!r}, "
                f"completed={self.completed!r}, created_at={self.created_at!r})")

    def to_dict(self) -> dict:
        """
        Convert the TodoItem to a dictionary representation.

        Returns:
            A dictionary with all the attributes of the TodoItem
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TodoItem':
        """
        Create a TodoItem from a dictionary representation.

        Args:
            data: Dictionary containing todo item data

        Returns:
            A new TodoItem instance
        """
        from datetime import datetime
        item = cls(
            description=data["description"],
            title=data.get("title", ""),
            todo_id=data["id"],
            completed=data["completed"]
        )
        item.created_at = datetime.fromisoformat(data["created_at"])
        return item