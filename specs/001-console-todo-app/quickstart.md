# Quickstart Guide: Console Todo App

## Setup

1. Ensure Python 3.8+ is installed on your system
2. Clone or create the project structure as defined in the implementation plan
3. No additional dependencies required beyond Python standard library

## Running the Application

```bash
uv run console_todo_app/main.py
```

## Development Workflow

1. Create unit tests first (TDD approach)
2. Implement the minimal functionality to pass tests
3. Refactor for code quality and maintainability
4. Run tests to ensure everything still works

## Key Components

- `todo_app/models/todo_item.py`: Contains the TodoItem model
- `todo_app/services/todo_service.py`: Contains business logic for todo operations
- `todo_app/cli/menu.py`: Contains the interactive menu interface
- `todo_app/main.py`: Application entry point

## Testing

Run all tests:
```bash
pytest tests/
```

Run specific test types:
```bash
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
```

## Common Commands

- Add a todo: Select option 1 from main menu and enter description
- View todos: Select option 2 from main menu
- Mark complete: Select option 3 and enter todo ID
- Update todo: Select option 4 and enter todo ID and new description
- Delete todo: Select option 5 and enter todo ID
- Exit: Select option 6 to quit the application