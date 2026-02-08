# Quickstart Guide: MCP Task Management Tools

## Overview
This guide provides instructions for setting up and running the MCP Task Management Tools server.

## Prerequisites
- Python 3.8 or higher
- Standard Python library (no external dependencies required)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Navigate to the MCP Server Directory
```bash
cd src/mcp_server
```

### 3. Run the MCP Server
```bash
python main.py
```

The server will start and begin listening for MCP tool requests.

## Using the Tools

### Add a Task
```python
# Example request to add_task
{
    "user_id": "ziakhan",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
}
```

Expected response:
```json
{
    "task_id": 5,
    "status": "created",
    "title": "Buy groceries"
}
```

### List Tasks
```python
# Example request to list_tasks
{
    "user_id": "ziakhan",
    "status": "pending"
}
```

Expected response:
```json
[
    {
        "id": 1,
        "title": "Buy groceries",
        "completed": false
    }
]
```

### Complete a Task
```python
# Example request to complete_task
{
    "user_id": "ziakhan",
    "task_id": 3
}
```

Expected response:
```json
{
    "task_id": 3,
    "status": "completed",
    "title": "Call mom"
}
```

### Delete a Task
```python
# Example request to delete_task
{
    "user_id": "ziakhan",
    "task_id": 2
}
```

Expected response:
```json
{
    "task_id": 2,
    "status": "deleted",
    "title": "Old task"
}
```

### Update a Task
```python
# Example request to update_task
{
    "user_id": "ziakhan",
    "task_id": 1,
    "title": "Buy groceries and fruits"
}
```

Expected response:
```json
{
    "task_id": 1,
    "status": "updated",
    "title": "Buy groceries and fruits"
}
```

## Configuration
The server uses in-memory storage by default. No additional configuration is required for basic operation.

## Troubleshooting
- If the server fails to start, ensure Python 3.8+ is installed
- Check that all required modules from the standard library are available
- Verify that the correct port is available for binding

## Next Steps
- Review the API contracts in the `contracts/` directory
- Examine the data models in `data-model.md`
- Look at the unit tests in the `tests/` directory for usage examples