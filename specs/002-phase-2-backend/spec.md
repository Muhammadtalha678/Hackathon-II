# Feature Specification: JWT Task Management API

**Feature Branch**: `002-phase-2-backend`
**Created**: 2026-01-07
**Status**: Draft
**Input**: User description: "Create RESTful API endpoints
GET
/api/{user_id}/tasks
List all tasks
POST
/api/{user_id}/tasks
Create a new task
GET
/api/{user_id}/tasks/{id}
Get task details
PUT
/api/{user_id}/tasks/{id}
Update a task
DELETE
/api/{user_id}/tasks/{id}
Delete a task
PATCH
/api/{user_id}/tasks/{id}/complete
Toggle completion

Backend receives request → Extracts token from header, verifies signature using shared secret
Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user
ID in the URL
Backend filters data → Returns only tasks belonging to that user
Add middleware to verify JWT and extract user
backend (FastAPI) must use the same secret key for JWT signing and verification. This is typically
set via environment variable BETTER_AUTH_SECRET in both services. API Behavior Change
After Auth:
All endpoints require valid JWT token
Requests without token receive 401 Unauthorized
Each user only sees/modifies their own tasks
Task ownership is enforced on every operation

Bottom Line
The REST API endpoints stay the same (GET /api/user_id/tasks, POST /api/user_id/tasks, etc.), but
every request now must include a JWT token, and all responses are filtered to only include that
user's data.
use @.claude\skills\fastapi-sqlmodel-backend-generator\SKILL.md to design specification"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Listing (Priority: P1)

As a registered user, I want to securely list all my tasks so that I can view my personal task data without seeing other users' information.

**Why this priority**: This is the core functionality that allows users to access their task data with proper authentication and authorization.

**Independent Test**: Can be fully tested by authenticating with a valid JWT token and verifying that only tasks belonging to the authenticated user are returned.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token and tasks in the system, **When** they make a GET request to /api/{user_id}/tasks with proper authentication, **Then** they receive a 200 OK response with only their tasks in the response body
2. **Given** a user has no JWT token, **When** they make a GET request to /api/{user_id}/tasks, **Then** they receive a 401 Unauthorized response

---

### User Story 2 - Secure Task Creation (Priority: P1)

As a registered user, I want to securely create new tasks so that I can add personal tasks to my account with proper authentication.

**Why this priority**: This enables users to add new tasks to their personal collection with security.

**Independent Test**: Can be fully tested by authenticating with a valid JWT token and creating a new task that is properly associated with the authenticated user.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token, **When** they make a POST request to /api/{user_id}/tasks with task data, **Then** they receive a 201 Created response with the new task properly associated with their user ID
2. **Given** a user has an invalid or expired JWT token, **When** they make a POST request to /api/{user_id}/tasks, **Then** they receive a 401 Unauthorized response

---

### User Story 3 - Secure Task Management (Priority: P2)

As a registered user, I want to securely view, update, delete, and toggle completion status of my tasks so that I can manage my personal task list.

**Why this priority**: This provides full CRUD functionality for users to manage their tasks with proper authentication.

**Independent Test**: Can be fully tested by authenticating with a valid JWT token and performing operations on tasks that belong to the authenticated user.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token and owns a specific task, **When** they make a GET request to /api/{user_id}/tasks/{id}, **Then** they receive a 200 OK response with the task details
2. **Given** a user has a valid JWT token and owns a specific task, **When** they make a PUT request to /api/{user_id}/tasks/{id}, **Then** they receive a 200 OK response with the updated task
3. **Given** a user has a valid JWT token and owns a specific task, **When** they make a DELETE request to /api/{user_id}/tasks/{id}, **Then** they receive a 200 OK response and the task is deleted
4. **Given** a user has a valid JWT token and owns a specific task, **When** they make a PATCH request to /api/{user_id}/tasks/{id}/complete, **Then** they receive a 200 OK response with the updated completion status

---

### Edge Cases

- What happens when a user tries to access another user's tasks?
- How does system handle invalid JWT tokens?
- What happens when a user tries to access a non-existent task?
- How does the system handle expired JWT tokens?
- What happens when the user ID in the URL doesn't match the user ID in the JWT token?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST require a valid JWT token in the request header for all task-related API endpoints
- **FR-002**: System MUST verify JWT token signature using the shared secret stored in BETTER_AUTH_SECRET environment variable
- **FR-003**: System MUST extract user ID from the JWT token and validate it matches the user ID in the URL
- **FR-004**: System MUST return 401 Unauthorized for requests without valid JWT tokens
- **FR-005**: System MUST only return tasks that belong to the authenticated user
- **FR-006**: System MUST allow users to create new tasks and associate them with their user ID
- **FR-007**: System MUST allow users to update their own tasks but not other users' tasks
- **FR-008**: System MUST allow users to delete their own tasks but not other users' tasks
- **FR-009**: System MUST allow users to toggle the completion status of their own tasks
- **FR-010**: System MUST implement middleware to verify JWT and extract user information
- **FR-011**: System MUST enforce task ownership on every operation to prevent unauthorized access

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with attributes like ID, title, description, completion status, and user ownership
- **User**: Represents a registered user with unique ID, authentication token, and associated tasks
- **JWT Token**: Authentication token containing user ID, email, and other user information with expiration

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can securely access their tasks with valid JWT tokens, with 99.9% success rate for authenticated requests
- **SC-002**: System properly rejects unauthorized requests with 401 status code within 100ms response time
- **SC-003**: Users can only access and modify their own tasks, with 0% cross-user data access incidents
- **SC-004**: Task operations (CRUD) complete successfully for authenticated users with 95% success rate
- **SC-005**: JWT token verification and user identification completes within 50ms for all authenticated requests