# Data Model: MCP Task Management Tools

## Overview
This document defines the data models for the MCP Task Management Tools system, based on the entities identified in the feature specification.

## Task Entity

### Attributes
- **task_id** (int): Unique identifier for the task; auto-generated; required
- **user_id** (str): Identifier for the user who owns the task; required
- **title** (str): Title of the task; required; min length 1 character
- **description** (str): Optional description of the task; nullable; max length 1000 characters
- **completed** (bool): Status indicating if the task is completed; default false
- **created_at** (datetime): Timestamp when the task was created; auto-generated
- **updated_at** (datetime): Timestamp when the task was last updated; auto-generated

### Validation Rules
- task_id must be unique within the system
- user_id must be a valid string identifier
- title must be between 1 and 255 characters
- completed must be a boolean value
- created_at and updated_at must be valid datetime objects

### State Transitions
- Initial state: completed = false
- Transition to completed: when complete_task tool is called
- No reverse transition from completed to incomplete (based on requirements)

## User Entity

### Attributes
- **user_id** (str): Unique identifier for the user; required; serves as primary identifier
- **created_at** (datetime): Timestamp when the user record was first accessed; auto-generated
- **tasks** (list): Collection of task_ids associated with the user; managed implicitly

### Validation Rules
- user_id must be unique within the system
- user_id must be a valid string identifier (alphanumeric + underscore/hyphen)
- Each user can have multiple associated tasks

### Relationships
- One User to Many Tasks (one-to-many relationship)
- Tasks are accessed/managed only by their owning user

## TaskList Entity

### Purpose
Virtual entity representing a filtered collection of tasks for a specific user based on status

### Attributes
- **user_id** (str): Identifier of the user whose tasks are being listed; required
- **status_filter** (str): Filter criteria ("all", "pending", "completed"); optional, defaults to "all"
- **tasks** (list): Array of Task objects matching the filter criteria

### Validation Rules
- user_id must correspond to an existing user
- status_filter must be one of: "all", "pending", "completed"
- Only tasks belonging to the specified user are included in results

## Constraints and Business Rules

### Access Control
- Users can only access their own tasks (user isolation requirement)
- Operations on tasks require matching user_id between the request and the task

### Data Integrity
- Task IDs are unique system-wide
- User IDs are unique system-wide
- Tasks cannot be transferred between users

### Performance
- Efficient lookup of tasks by user_id
- Efficient filtering of tasks by completion status
- Reasonable limits on number of tasks per user (10,000 as per spec)