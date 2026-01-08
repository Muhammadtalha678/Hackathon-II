# Data Model: JWT Task Management API

## Entity: User
**Description**: Represents a registered user with authentication information

**Fields**:
- `id` (UUID/Integer): Unique identifier for the user (primary key)
- `email` (String): User's email address for identification
- `hashed_password` (String): BCrypt hashed password for authentication
- `created_at` (DateTime): Timestamp when user account was created
- `updated_at` (DateTime): Timestamp when user account was last updated
- `is_active` (Boolean): Flag indicating if user account is active

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet security requirements (handled during hashing)

## Entity: Task
**Description**: Represents a user's task with attributes and completion status

**Fields**:
- `id` (UUID/Integer): Unique identifier for the task (primary key)
- `title` (String): Task title/description (required)
- `description` (Text): Detailed description of the task (optional)
- `is_completed` (Boolean): Flag indicating if task is completed (default: False)
- `user_id` (UUID/Integer): Foreign key linking to the owning user
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp when task was last updated

**Validation Rules**:
- Title must be provided and not empty
- User ID must reference an existing user
- Only the task owner can modify the task

## Relationships
- **User → Task**: One-to-Many relationship
  - One user can have many tasks
  - Each task belongs to exactly one user
  - When a user is deleted, their tasks should also be deleted (cascade deletion)

## Business Logic Constraints
- Task visibility: Users can only see, modify, or delete their own tasks
- Task ownership: When creating a task, the authenticated user ID is automatically assigned as the owner
- Data isolation: API endpoints enforce user-specific filtering

## State Transitions
### Task Completion
- Initial state: `is_completed = False`
- Action: PATCH `/api/{user_id}/tasks/{id}/complete`
- Transition: Toggle `is_completed` field between True and False
- Validation: Only task owner can toggle completion status

## Indexes for Performance
- User.email: For efficient user lookup during authentication
- Task.user_id: For efficient user-specific task filtering
- Task.created_at: For sorting and pagination of tasks