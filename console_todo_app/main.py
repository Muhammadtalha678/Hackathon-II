#!/usr/bin/env python3
"""
Console Todo App - Main entry point

This is the main application file for the Console Todo App.
"""
from src.services.todo_service import TodoService
from src.cli.menu import Menu


def main():
    """Main function to run the Console Todo App."""
    print("Welcome to Todo Manager!")

    # Initialize the todo service and menu
    todo_service = TodoService()
    menu = Menu(todo_service)

    # Main application loop
    while True:
        menu.display_menu()
        choice = menu.get_user_choice()

        if choice == '2':
            menu.handle_add_todo()
        elif choice == '1':
            menu.handle_view_todos()
        elif choice == '3':
            menu.handle_mark_complete()
        elif choice == '4':
            menu.handle_update_todo()
        elif choice == '5':
            menu.handle_delete_todo()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            menu.handle_invalid_choice(choice)


if __name__ == "__main__":
    main()
