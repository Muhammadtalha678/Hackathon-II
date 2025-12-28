"""
Integration tests for the CLI menu navigation.

This module contains integration tests for the menu navigation functionality
to ensure all menu options work correctly together.
"""
from unittest.mock import Mock, patch
from src.services.todo_service import TodoService
from src.cli.menu import Menu


class TestCLIIntegration:
    """
    Test class for CLI menu navigation integration.
    """

    def test_menu_display_and_navigation_options(self):
        """
        Test that the menu displays all required options correctly.
        """
        service = TodoService()
        menu = Menu(service)

        # Capture the menu display output by checking if all expected options are present
        import io
        import sys
        from contextlib import redirect_stdout

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            menu.display_menu()

        output = captured_output.getvalue()

        # Check that all menu options are present
        assert "Add Todo" in output
        assert "View Todos" in output
        assert "Mark Complete" in output
        assert "Update Todo" in output
        assert "Delete Todo" in output
        assert "Exit" in output

    def test_add_and_view_integration(self):
        """
        Test adding a todo and then viewing it.
        """
        service = TodoService()
        menu = Menu(service)

        # Add a todo using the menu's method
        description = "Test integration todo"

        # Mock the input to simulate user entering the description
        with patch('builtins.input', return_value=description):
            menu.handle_add_todo()

        # Verify the todo was added to the service
        todos = service.get_all_todos()
        assert len(todos) == 1
        assert todos[0].description == description

        # Now view the todos using the menu's method
        import io
        import sys
        from contextlib import redirect_stdout

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            menu.handle_view_todos()

        output = captured_output.getvalue()
        assert description in output

    def test_add_view_and_delete_integration(self):
        """
        Test adding a todo, viewing it, and then deleting it.
        """
        service = TodoService()
        menu = Menu(service)

        # Add a todo
        description = "Test delete integration todo"
        with patch('builtins.input', return_value=description):
            menu.handle_add_todo()

        # Verify it was added
        todos = service.get_all_todos()
        assert len(todos) == 1
        todo_id = todos[0].id
        assert todo_id is not None

        # Now delete the todo by mocking the input for ID
        with patch('builtins.input', return_value=todo_id):
            menu.handle_delete_todo()

        # Verify it was deleted
        todos = service.get_all_todos()
        assert len(todos) == 0

    def test_add_and_mark_complete_integration(self):
        """
        Test adding a todo and then marking it as complete.
        """
        service = TodoService()
        menu = Menu(service)

        # Add a todo
        description = "Test complete integration todo"
        with patch('builtins.input', return_value=description):
            menu.handle_add_todo()

        # Get the todo to get its ID
        todos = service.get_all_todos()
        assert len(todos) == 1
        todo_id = todos[0].id
        assert not todos[0].completed  # Should be incomplete initially

        # Mark as complete
        with patch('builtins.input', return_value=todo_id):
            menu.handle_mark_complete()

        # Verify it was marked as complete
        todos = service.get_all_todos()
        assert len(todos) == 1
        assert todos[0].completed

    def test_invalid_menu_choice_handling(self):
        """
        Test that invalid menu choices are handled properly.
        """
        service = TodoService()
        menu = Menu(service)

        import io
        import sys
        from contextlib import redirect_stdout

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            menu.handle_invalid_choice("999")

        output = captured_output.getvalue()
        assert "Invalid choice" in output
        assert "999" in output
        assert "number between 1 and 6" in output