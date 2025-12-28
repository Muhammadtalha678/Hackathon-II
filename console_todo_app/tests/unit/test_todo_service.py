"""
Unit tests for the TodoService add_todo functionality.

This module contains unit tests for the TodoService's add_todo method
to ensure it functions correctly according to the specifications.
"""
import pytest
from src.services.todo_service import TodoService
from src.models.todo_item import TodoItem


class TestTodoServiceAddTodo:
    """
    Test class for TodoService add_todo functionality.
    """

    def test_add_todo_with_valid_description(self):
        """
        Test adding a todo with a valid description.
        """
        service = TodoService()
        description = "Test todo item"

        result = service.add_todo(description)

        assert isinstance(result, TodoItem)
        assert result.description == description
        assert result.title == description  # Title defaults to description if not provided
        assert result.completed is False
        assert result.id is not None
        assert len(service.todos) == 1
        assert service.todos[0] == result

    def test_add_todo_generates_sequential_ids(self):
        """
        Test that adding multiple todos generates sequential IDs.
        """
        service = TodoService()

        todo1 = service.add_todo("First todo")
        todo2 = service.add_todo("Second todo")

        assert todo1.id == "1"
        assert todo2.id == "2"
        assert len(service.todos) == 2

    def test_add_todo_with_empty_description_raises_error(self):
        """
        Test that adding a todo with an empty description raises ValueError.
        """
        service = TodoService()

        with pytest.raises(ValueError, match="Description cannot be empty or whitespace only"):
            service.add_todo("")

    def test_add_todo_with_whitespace_only_description_raises_error(self):
        """
        Test that adding a todo with whitespace-only description raises ValueError.
        """
        service = TodoService()

        with pytest.raises(ValueError, match="Description cannot be empty or whitespace only"):
            service.add_todo("   ")

    def test_add_todo_with_long_description_raises_error(self):
        """
        Test that adding a todo with a description over 500 chars raises ValueError.
        """
        service = TodoService()
        long_description = "x" * 501

        with pytest.raises(ValueError, match="Description must be under 500 characters"):
            service.add_todo(long_description)

    def test_add_todo_adds_to_internal_list(self):
        """
        Test that adding a todo properly adds it to the internal list.
        """
        service = TodoService()
        description = "Test todo item"

        result = service.add_todo(description)

        assert len(service.todos) == 1
        assert service.todos[0] == result
        assert service.todos[0].description == description
        assert service.todos[0].title == description  # Title defaults to description

    def test_add_todo_with_title(self):
        """
        Test adding a todo with both description and title.
        """
        service = TodoService()
        description = "Test todo item description"
        title = "Test Title"

        result = service.add_todo(description, title)

        assert isinstance(result, TodoItem)
        assert result.description == description
        assert result.title == title
        assert result.completed is False
        assert result.id is not None
        assert len(service.todos) == 1
        assert service.todos[0] == result


class TestTodoServiceGetAllTodos:
    """
    Test class for TodoService get_all_todos functionality.
    """

    def test_get_all_todos_empty_list(self):
        """
        Test getting all todos when the list is empty.
        """
        service = TodoService()

        todos = service.get_all_todos()

        assert isinstance(todos, list)
        assert len(todos) == 0

    def test_get_all_todos_single_item(self):
        """
        Test getting all todos when there's one item.
        """
        service = TodoService()
        description = "Test todo item"
        added_todo = service.add_todo(description)

        todos = service.get_all_todos()

        assert len(todos) == 1
        assert todos[0] == added_todo
        assert todos[0].description == description

    def test_get_all_todos_multiple_items(self):
        """
        Test getting all todos when there are multiple items.
        """
        service = TodoService()
        service.add_todo("First todo")
        service.add_todo("Second todo")
        service.add_todo("Third todo")

        todos = service.get_all_todos()

        assert len(todos) == 3
        assert all(isinstance(todo, TodoItem) for todo in todos)

    def test_get_all_todos_returns_copy_not_original(self):
        """
        Test that get_all_todos returns a copy, not the original list.
        """
        service = TodoService()
        service.add_todo("Test todo")

        todos = service.get_all_todos()

        # Modify the returned list
        original_length = len(todos)
        todos.append("This should not affect the service's list")

        # Check that the service's internal list is unchanged
        assert len(service.get_all_todos()) == original_length


class TestTodoServiceMarkComplete:
    """
    Test class for TodoService mark_complete functionality.
    """

    def test_mark_complete_existing_todo(self):
        """
        Test marking an existing todo as complete.
        """
        service = TodoService()
        todo = service.add_todo("Test todo")

        result = service.mark_complete(todo.id)

        assert result is True
        assert todo.completed is True

    def test_mark_complete_nonexistent_todo(self):
        """
        Test marking a nonexistent todo as complete.
        """
        service = TodoService()

        result = service.mark_complete("nonexistent-id")

        assert result is False

    def test_mark_incomplete_existing_todo(self):
        """
        Test marking an existing todo as incomplete.
        """
        service = TodoService()
        todo = service.add_todo("Test todo")
        # First mark as complete
        service.mark_complete(todo.id)

        result = service.mark_incomplete(todo.id)

        assert result is True
        assert todo.completed is False

    def test_mark_incomplete_nonexistent_todo(self):
        """
        Test marking a nonexistent todo as incomplete.
        """
        service = TodoService()

        result = service.mark_incomplete("nonexistent-id")

        assert result is False

    def test_mark_complete_then_incomplete(self):
        """
        Test marking a todo as complete then incomplete.
        """
        service = TodoService()
        todo = service.add_todo("Test todo")

        # Mark as complete
        service.mark_complete(todo.id)
        assert todo.completed is True

        # Mark as incomplete
        service.mark_incomplete(todo.id)
        assert todo.completed is False


class TestTodoServiceDeleteTodo:
    """
    Test class for TodoService delete_todo functionality.
    """

    def test_delete_existing_todo(self):
        """
        Test deleting an existing todo.
        """
        service = TodoService()
        todo = service.add_todo("Test todo to delete")

        result = service.delete_todo(todo.id)

        assert result is True
        assert len(service.get_all_todos()) == 0

    def test_delete_nonexistent_todo(self):
        """
        Test deleting a nonexistent todo.
        """
        service = TodoService()

        result = service.delete_todo("nonexistent-id")

        assert result is False
        assert len(service.get_all_todos()) == 0

    def test_delete_one_of_multiple_todos(self):
        """
        Test deleting one todo from a list of multiple todos.
        """
        service = TodoService()
        first_todo = service.add_todo("First todo")
        second_todo = service.add_todo("Second todo")
        third_todo = service.add_todo("Third todo")

        # Delete the second todo
        result = service.delete_todo(second_todo.id)

        assert result is True
        todos = service.get_all_todos()
        assert len(todos) == 2
        assert first_todo in todos
        assert third_todo in todos
        assert second_todo not in todos

    def test_delete_todo_twice(self):
        """
        Test deleting the same todo twice.
        """
        service = TodoService()
        todo = service.add_todo("Test todo to delete twice")

        # First deletion should succeed
        result1 = service.delete_todo(todo.id)
        assert result1 is True

        # Second deletion should fail
        result2 = service.delete_todo(todo.id)
        assert result2 is False


class TestTodoServiceUpdateTodo:
    """
    Test class for TodoService update_todo functionality.
    """

    def test_update_existing_todo(self):
        """
        Test updating an existing todo's description.
        """
        service = TodoService()
        original_description = "Original description"
        new_description = "New description"
        todo = service.add_todo(original_description)

        result = service.update_todo(todo.id, new_description)

        assert result is True
        assert todo.description == new_description

    def test_update_existing_todo_with_title(self):
        """
        Test updating an existing todo's description and title.
        """
        service = TodoService()
        original_description = "Original description"
        original_title = "Original Title"
        new_description = "New description"
        new_title = "New Title"
        todo = service.add_todo(original_description, original_title)

        result = service.update_todo(todo.id, new_description, new_title)

        assert result is True
        assert todo.description == new_description
        assert todo.title == new_title

    def test_update_nonexistent_todo(self):
        """
        Test updating a nonexistent todo.
        """
        service = TodoService()
        new_description = "New description"

        result = service.update_todo("nonexistent-id", new_description)

        assert result is False

    def test_update_todo_with_empty_description_raises_error(self):
        """
        Test updating a todo with an empty description raises ValueError.
        """
        service = TodoService()
        original_description = "Original description"
        todo = service.add_todo(original_description)

        with pytest.raises(ValueError, match="Description cannot be empty or whitespace only"):
            service.update_todo(todo.id, "")

    def test_update_todo_with_whitespace_only_description_raises_error(self):
        """
        Test updating a todo with whitespace-only description raises ValueError.
        """
        service = TodoService()
        original_description = "Original description"
        todo = service.add_todo(original_description)

        with pytest.raises(ValueError, match="Description cannot be empty or whitespace only"):
            service.update_todo(todo.id, "   ")

    def test_update_todo_with_long_description_raises_error(self):
        """
        Test updating a todo with a description over 500 chars raises ValueError.
        """
        service = TodoService()
        original_description = "Original description"
        todo = service.add_todo(original_description)
        long_description = "x" * 501

        with pytest.raises(ValueError, match="Description must be under 500 characters"):
            service.update_todo(todo.id, long_description)