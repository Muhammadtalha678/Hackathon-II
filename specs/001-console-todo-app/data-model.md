# Data Model: Console Todo App

## Overview
This document defines the data models for the Phase I Console Todo App, based on the entities identified in the feature specification.

## TodoItem Entity

### Attributes
- **id**: `str` - Unique identifier for the todo item (generated using uuid)
- **description**: `str` - Text description of the task
- **completed**: `bool` - Status indicating whether the task is completed (default: False)
- **created_at**: `datetime` - Timestamp when the todo was created

### Validation Rules
- `description` must not be empty or whitespace-only (from FR-010)
- `description` must be a string with reasonable length limit (e.g., max 500 characters)
- `id` must be unique within the todo list
- `completed` is a boolean value only

### State Transitions
- `completed` can transition from `False` to `True` (mark complete)
- `completed` can transition from `True` to `False` (mark incomplete)

## TodoList Entity

### Attributes
- **items**: `List[TodoItem]` - Collection of TodoItem objects
- **next_id**: `int` - Counter for generating unique IDs (optional, could use uuid)

### Operations
- **add_item**(description: str) -> TodoItem: Creates and adds a new TodoItem to the list
- **get_all_items**() -> List[TodoItem]: Returns all items in the list
- **get_item_by_id**(id: str) -> Optional[TodoItem]: Returns item with matching ID or None
- **update_item**(id: str, new_description: str) -> bool: Updates description of existing item
- **mark_complete**(id: str) -> bool: Marks item as completed
- **mark_incomplete**(id: str) -> bool: Marks item as incomplete
- **delete_item**(id: str) -> bool: Removes item from the list

### Validation Rules
- All operations must validate that the item ID exists before performing operations (addresses edge cases from spec)
- `update_item`, `mark_complete`, `mark_incomplete`, and `delete_item` return False if item doesn't exist
- Empty list handling is supported (addresses edge cases from spec)

## Relationships
- TodoList contains 0 or more TodoItem objects
- Each TodoItem belongs to exactly one TodoList during the application session