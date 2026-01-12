# Data Model: Next.js Frontend with Authentication and Task Management

## Entity: User
**Source**: Better Auth integration with Neon database
**Persistence**: Server-side via Better Auth

### Fields:
- `id` (string/number): Unique identifier for the user
- `name` (string): User's display name
- `email` (string): User's email address (unique)
- `password` (string): Hashed password (server-side only)
- `is_active` (boolean): Account active status
- `created_at` (timestamp): Account creation timestamp
- `updated_at` (timestamp): Last update timestamp

### Relationships:
- One-to-many with Task entities (via user_id foreign key)

### Validation Rules:
- Email must be unique
- Name required during registration
- Password must meet security requirements (handled by Better Auth)

## Entity: Task
**Source**: FastAPI backend database
**Persistence**: Server-side via FastAPI backend

### Fields:
- `id` (integer): Unique identifier for the task
- `title` (string): Task title (required, 1-500 characters)
- `description` (string | null): Task description (optional, max 2000 characters)
- `is_completed` (boolean): Completion status (default: false)
- `user_id` (integer): Foreign key to User
- `created_at` (timestamp): Task creation timestamp
- `updated_at` (timestamp): Last update timestamp

### Relationships:
- Many-to-one with User (belongs to one user)

### Validation Rules:
- Title required (min 1 character, max 500 characters)
- Description optional (max 2000 characters)
- is_completed defaults to false
- user_id must reference valid user

## Entity: Session
**Source**: Better Auth session management
**Persistence**: Server-side via Better Auth

### Fields:
- `id` (string): Unique session identifier
- `user_id` (string/number): Reference to authenticated user
- `expires_at` (timestamp): Session expiration time
- `created_at` (timestamp): Session creation timestamp

### Relationships:
- Many-to-one with User (belongs to one user)

## Entity: Authentication Token (JWT)
**Source**: Better Auth JWT generation
**Persistence**: Client-side in browser (temporary), server-side validation

### Fields:
- `token` (string): JWT token string
- `user_id` (string/number): Embedded user identifier
- `expires_at` (timestamp): Token expiration time
- `issued_at` (timestamp): Token issuance time

### Relationships:
- One-to-one with Session during validation

## State Transitions

### Task State Transitions:
1. **Created**: Task is created with `is_completed: false`
2. **Updated**: Task details can be modified (title, description)
3. **Completed**: `is_completed` toggled to `true`
4. **Reopened**: `is_completed` toggled back to `false` (if needed)
5. **Deleted**: Task is removed from user's list

### Session State Transitions:
1. **Authenticated**: User logs in, session created
2. **Active**: User interacts with application
3. **Expired**: Token expires, automatic logout
4. **Logged Out**: User explicitly logs out

## API Response Models

### Task Response Model:
```typescript
interface Task {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  user_id: number;
  created_at: string; // ISO timestamp
  updated_at: string; // ISO timestamp
}
```

### Task List Response Model:
```typescript
type TaskList = Task[];
```

### Task Creation Response Model:
```typescript
interface TaskCreationResponse extends Task {}
```

### Task Update Response Model:
```typescript
interface TaskUpdateResponse extends Task {}
```

### Task Deletion Response Model:
```typescript
interface TaskDeletionResponse {
  success: boolean;
  message: string;
  deleted_id: number;
}
```

### User Profile Response Model:
```typescript
interface UserProfile {
  id: string | number;
  name: string;
  email: string;
  is_active: boolean;
}
```

### Authentication Response Model:
```typescript
interface AuthResponse {
  user: UserProfile;
  token: string;
}
```

## Frontend Data Models

### Local State Models:
```typescript
interface TaskFormData {
  title: string;
  description: string | null;
  is_completed: boolean;
}

interface UserProfileFormData {
  name: string;
}

interface PasswordChangeFormData {
  oldPassword: string;
  newPassword: string;
  confirmNewPassword: string;
}
```

### Validation Models:
```typescript
interface TaskValidationRules {
  title: {
    required: true;
    minLength: 1;
    maxLength: 500;
  };
  description: {
    maxLength: 2000;
  };
}

interface PasswordValidationRules {
  oldPassword: {
    required: true;
  };
  newPassword: {
    required: true;
    minLength: 8;
  };
  confirmNewPassword: {
    required: true;
    matchesNewPassword: true;
  };
}
```