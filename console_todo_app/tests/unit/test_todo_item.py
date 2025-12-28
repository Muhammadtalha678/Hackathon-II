"""
Unit tests for the TodoItem model.

This module contains unit tests for the TodoItem class to ensure
it functions correctly according to the specifications.
"""
import pytest
from datetime import datetime
from src.models.todo_item import TodoItem


class TestTodoItem:
    """
    Test class for TodoItem model.
    """

    def test_create_todo_item_with_valid_description(self):
        """
        Test creating a TodoItem with a valid description.
        """
        description = "Test todo item"
        todo = TodoItem(description=description)

        assert todo.description == description
        assert todo.title == description  # Title defaults to description if not provided
        assert todo.completed is False
        assert todo.id is None  # ID is set externally
        assert isinstance(todo.created_at, datetime)

    def test_create_todo_item_with_custom_id(self):
        """
        Test creating a TodoItem with a custom ID.
        """
        description = "Test todo item"
        custom_id = "custom-123"
        todo = TodoItem(description=description, todo_id=custom_id)

        assert todo.id == custom_id
        assert todo.description == description
        assert todo.title == description  # Title defaults to description if not provided

    def test_create_todo_item_with_title(self):
        """
        Test creating a TodoItem with a custom title.
        """
        description = "Test todo item description"
        title = "Test Title"
        custom_id = "custom-123"
        todo = TodoItem(description=description, title=title, todo_id=custom_id)

        assert todo.id == custom_id
        assert todo.description == description
        assert todo.title == title

    def test_create_todo_item_completed_by_default(self):
        """
        Test creating a TodoItem with completed status set to True.
        """
        description = "Test todo item"
        todo = TodoItem(description=description, completed=True)

        assert todo.completed is True

    def test_create_todo_item_with_empty_description_raises_error(self):
        """
        Test that creating a TodoItem with an empty description raises ValueError.
        """
        with pytest.raises(ValueError, match="Description cannot be empty or whitespace only"):
            TodoItem(description="")

    def test_create_todo_item_with_whitespace_only_description_raises_error(self):
        """
        Test that creating a TodoItem with whitespace-only description raises ValueError.
        """
        with pytest.raises(ValueError, match="Description cannot be empty or whitespace only"):
            TodoItem(description="   ")

    def test_create_todo_item_with_long_description_raises_error(self):
        """
        Test that creating a TodoItem with a description over 500 chars raises ValueError.
        """
        long_description = "x" * 501
        with pytest.raises(ValueError, match="Description must be under 500 characters"):
            TodoItem(description=long_description)

    def test_todo_item_str_representation(self):
        """
        Test the string representation of a TodoItem.
        """
        description = "Test todo item"
        todo = TodoItem(description=description, todo_id="123")

        str_repr = str(todo)
        assert "123" in str_repr
        assert description in str_repr
        assert "○" in str_repr  # Uncompleted task marker

    def test_todo_item_str_representation_completed(self):
        """
        Test the string representation of a completed TodoItem.
        """
        description = "Test todo item"
        todo = TodoItem(description=description, todo_id="123", completed=True)

        str_repr = str(todo)
        assert "123" in str_repr
        assert description in str_repr
        assert "✓" in str_repr  # Completed task marker

    def test_todo_item_repr_representation(self):
        """
        Test the developer representation of a TodoItem.
        """
        description = "Test todo item"
        todo = TodoItem(description=description, todo_id="123")

        repr_str = repr(todo)
        assert "TodoItem" in repr_str
        assert "123" in repr_str
        assert description in repr_str

    def test_todo_item_to_dict(self):
        """
        Test converting a TodoItem to dictionary representation.
        """
        description = "Test todo item"
        todo = TodoItem(description=description, todo_id="123")
        todo_dict = todo.to_dict()

        assert todo_dict["id"] == "123"
        assert todo_dict["description"] == description
        assert todo_dict["completed"] is False
        assert "created_at" in todo_dict

    def test_todo_item_from_dict(self):
        """
        Test creating a TodoItem from dictionary representation.
        """
        original_data = {
            "id": "123",
            "description": "Test todo item",
            "completed": True,
            "created_at": datetime.now().isoformat()
        }

        todo = TodoItem.from_dict(original_data)

        assert todo.id == original_data["id"]
        assert todo.description == original_data["description"]
        assert todo.completed == original_data["completed"]