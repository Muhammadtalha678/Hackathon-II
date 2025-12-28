# Todo Manager

A simple and intuitive command-line todo application that helps you manage your tasks efficiently.

## Features

- **Add Tasks**: Create new tasks with titles and descriptions
- **View Tasks**: See all your tasks in a clean, organized table
- **Mark Complete/Incomplete**: Toggle task status with a single command
- **Update Tasks**: Modify existing task titles and descriptions
- **Delete Tasks**: Remove tasks you no longer need
- **Sequential IDs**: Simple numeric IDs (1, 2, 3, etc.) for easy reference
- **Detailed View**: Shows task status, ID, title, and creation date

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `uv` package manager (optional, but recommended)

### Installation

1. Clone or download this repository
2. Navigate to the `console_todo_app` directory
3. Install dependencies:
   ```bash
   uv sync  # If using uv
   # or
   pip install -r requirements.txt  # If using pip
   ```

### Running the Application

```bash
cd console_todo_app
python main.py
```

## Usage

Once you run the application, you'll see the main menu:

```
=== Todo Manager ===
1. View all tasks
2. Add new task
3. Mark task as complete/incomplete
4. Update task
5. Delete task
6. Exit
```

### Adding a Task

1. Select option `2` to add a new task
2. Enter the task title when prompted
3. Enter an optional description
4. The task will be added with a sequential ID

### Viewing Tasks

1. Select option `1` to view all tasks
2. Tasks are displayed in a table format with:
   - ID: Sequential number (1, 2, 3, etc.)
   - Status: `[ ]` for pending, `[x]` for completed
   - Title: The task title
   - Created: Date and time when the task was created

### Marking Tasks Complete/Incomplete

1. Select option `3` to toggle task completion status
2. View the current list of tasks
3. Enter the ID of the task you want to toggle
4. The task status will switch between complete/incomplete

### Updating a Task

1. Select option `4` to update a task
2. View the current list of tasks
3. Enter the ID of the task you want to update
4. Enter new title and/or description when prompted

### Deleting a Task

1. Select option `5` to delete a task
2. View the current list of tasks
3. Enter the ID of the task you want to delete
4. Confirm the deletion when prompted

## Project Structure

```
console_todo_app/
├── main.py                 # Main application entry point
├── src/
│   ├── models/
│   │   └── todo_item.py   # TodoItem model definition
│   ├── services/
│   │   └── todo_service.py # Business logic for todo operations
│   └── cli/
│       └── menu.py         # Interactive menu interface
├── tests/
│   ├── unit/
│   │   ├── test_todo_item.py
│   │   └── test_todo_service.py
│   └── integration/
│       └── test_cli_integration.py
└── README.md
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Architecture

The application follows a clean architecture pattern:

- **Models**: Data structures and business objects (`TodoItem`)
- **Services**: Business logic and operations (`TodoService`)
- **CLI**: User interface and interaction (`Menu`)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).