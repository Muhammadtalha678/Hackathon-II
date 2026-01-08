# API Contract: Task Management Endpoints

## Base URL
`/api/{user_id}`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```
Or in the access_token cookie.

## Endpoints

### GET /api/{user_id}/tasks
**Description**: List all tasks for the specified user

**Path Parameters**:
- `user_id` (string): The ID of the user whose tasks to retrieve

**Headers**:
- `Authorization`: Bearer token with valid JWT

**Response**:
- `200 OK`: Successfully retrieved tasks
  ```json
  {
    "tasks": [
      {
        "id": "task-uuid",
        "title": "Task title",
        "description": "Task description",
        "is_completed": false,
        "user_id": "user-uuid",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
      }
    ]
  }
  ```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in token doesn't match user ID in URL
- `404 Not Found`: User with specified ID doesn't exist

---

### POST /api/{user_id}/tasks
**Description**: Create a new task for the specified user

**Path Parameters**:
- `user_id` (string): The ID of the user to create task for

**Headers**:
- `Authorization`: Bearer token with valid JWT

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Task description"
}
```

**Response**:
- `201 Created`: Task successfully created
  ```json
  {
    "id": "task-uuid",
    "title": "Task title",
    "description": "Task description",
    "is_completed": false,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
  ```

**Error Responses**:
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in token doesn't match user ID in URL
- `404 Not Found`: User with specified ID doesn't exist

---

### GET /api/{user_id}/tasks/{id}
**Description**: Get details of a specific task

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (string): The ID of the task to retrieve

**Headers**:
- `Authorization`: Bearer token with valid JWT

**Response**:
- `200 OK`: Task details successfully retrieved
  ```json
  {
    "id": "task-uuid",
    "title": "Task title",
    "description": "Task description",
    "is_completed": false,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
  ```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in token doesn't match user ID in URL
- `404 Not Found`: Task or user doesn't exist

---

### PUT /api/{user_id}/tasks/{id}
**Description**: Update a specific task

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (string): The ID of the task to update

**Headers**:
- `Authorization`: Bearer token with valid JWT

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "is_completed": true
}
```

**Response**:
- `200 OK`: Task successfully updated
  ```json
  {
    "id": "task-uuid",
    "title": "Updated task title",
    "description": "Updated task description",
    "is_completed": true,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z"
  }
  ```

**Error Responses**:
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in token doesn't match user ID in URL
- `404 Not Found`: Task or user doesn't exist

---

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (string): The ID of the task to delete

**Headers**:
- `Authorization`: Bearer token with valid JWT

**Response**:
- `200 OK`: Task successfully deleted
  ```json
  {
    "message": "Task deleted successfully"
  }
  ```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in token doesn't match user ID in URL
- `404 Not Found`: Task or user doesn't exist

---

### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Toggle the completion status of a specific task

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (string): The ID of the task to update

**Headers**:
- `Authorization`: Bearer token with valid JWT

**Response**:
- `200 OK`: Task completion status successfully toggled
  ```json
  {
    "id": "task-uuid",
    "title": "Task title",
    "description": "Task description",
    "is_completed": true,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z"
  }
  ```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in token doesn't match user ID in URL
- `404 Not Found`: Task or user doesn't exist