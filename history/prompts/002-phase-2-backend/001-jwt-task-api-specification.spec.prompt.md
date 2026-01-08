---
id: 001
title: jwt-task-api-specification
stage: spec
date: 2026-01-07
surface: agent
model: Claude Sonnet 4.5
feature: 002-phase-2-backend
branch: 002-phase-2-backend
user: Claude Code User
command: /sp.specify
labels: ["api", "jwt", "authentication", "tasks", "specification"]
spec: specs/002-phase-2-backend/spec.md
ticket: null
adr: null
pr: null
files:
  - specs/002-phase-2-backend/spec.md
  - specs/002-phase-2-backend/checklists/requirements.md
tests: []
---

# PHR: jwt-task-api-specification

## Prompt

```
Create RESTful API endpoints
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
/api/{user_id}tasks/{id}
Delete a task
PATCH
/api/{user_id}tasks/{id}/complete
Toggle completioncompletion

Backend receives request → Extracts token from header, verifies signature using shared secret
Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user
ID
 in the URL
Backend filters data → Returns only tasks belonging to that user
Add middleware to verify JWT and extract user
backend (FastAPI) must use the same secret key for JWT signing and verification. This is typically
set via environment variable BETTER_AUTH_SECRET in both services.API Behavior Change
After Auth:
All endpoints require valid JWT token
Requests without token receive 401 Unauthorized
Each user only sees/modifies their own tasks
Task ownership is enforced on every operation

Bottom Line
The REST API endpoints stay the same (GET /api/user_id/tasks, POST /api/user_id/tasks, etc.), but
every request now must include a JWT token, and all responses are filtered to only include that
user's data.
use @.claude\skills\fastapi-sqlmodel-backend-generator\SKILL.md to design specification
```

## Response

Created a comprehensive specification for a JWT Task Management API with the following key elements:

### User Scenarios & Testing
- Secure Task Listing (P1 priority) - Allow users to list their own tasks with JWT authentication
- Secure Task Creation (P1 priority) - Allow users to create tasks with proper authentication
- Secure Task Management (P2 priority) - Full CRUD operations with JWT authentication

### Functional Requirements
- JWT token requirement for all endpoints
- Token signature verification using BETTER_AUTH_SECRET
- User ID validation and matching
- 401 Unauthorized responses for invalid tokens
- User-specific task filtering
- Task ownership enforcement

### Success Criteria
- 99.9% success rate for authenticated requests
- Proper rejection of unauthorized requests
- Zero cross-user data access incidents
- 95% success rate for task operations
- 50ms JWT verification time

## Outcome

Successfully created a comprehensive feature specification in `specs/002-phase-2-backend/spec.md` that defines a JWT-authenticated task management API. The specification includes user scenarios, functional requirements, key entities, and success criteria. A quality checklist was also created to validate the specification meets all requirements.

## Evaluation

The specification is complete, testable, and technology-agnostic. It properly addresses all the requirements from the user input, including JWT authentication, user-specific data access, and the required API endpoints. The specification is ready for the planning phase.