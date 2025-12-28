# API Contracts: Console Todo App

## Overview
This document defines the API contracts for the Console Todo App operations, representing the interface between the CLI layer and the service layer.

## Core Operations

### Add Todo
- **Method**: `todo_service.add_todo(description: str) -> TodoItem`
- **Input**: description (string, required)
- **Output**: TodoItem object with all attributes populated
- **Validation**:
  - Description must not be empty or whitespace-only
  - Description must be under 500 characters
- **Error Cases**:
  - ValueError if description is invalid

### View All Todos
- **Method**: `todo_service.get_all_todos() -> List[TodoItem]`
- **Input**: None
- **Output**: List of TodoItem objects, empty list if no items
- **Validation**: None
- **Error Cases**: None

### Get Todo by ID
- **Method**: `todo_service.get_todo_by_id(todo_id: str) -> Optional[TodoItem]`
- **Input**: todo_id (string, required)
- **Output**: TodoItem object if found, None if not found
- **Validation**: ID must exist in the todo list
- **Error Cases**: None (returns None for non-existent ID)

### Update Todo
- **Method**: `todo_service.update_todo(todo_id: str, new_description: str) -> bool`
- **Input**: todo_id (string, required), new_description (string, required)
- **Output**: True if update successful, False if todo not found
- **Validation**:
  - ID must exist in the todo list
  - New description must not be empty or whitespace-only
- **Error Cases**: None (returns False for non-existent ID)

### Mark Complete
- **Method**: `todo_service.mark_complete(todo_id: str) -> bool`
- **Input**: todo_id (string, required)
- **Output**: True if mark successful, False if todo not found
- **Validation**: ID must exist in the todo list
- **Error Cases**: None (returns False for non-existent ID)

### Mark Incomplete
- **Method**: `todo_service.mark_incomplete(todo_id: str) -> bool`
- **Input**: todo_id (string, required)
- **Output**: True if mark successful, False if todo not found
- **Validation**: ID must exist in the todo list
- **Error Cases**: None (returns False for non-existent ID)

### Delete Todo
- **Method**: `todo_service.delete_todo(todo_id: str) -> bool`
- **Input**: todo_id (string, required)
- **Output**: True if delete successful, False if todo not found
- **Validation**: ID must exist in the todo list
- **Error Cases**: None (returns False for non-existent ID)