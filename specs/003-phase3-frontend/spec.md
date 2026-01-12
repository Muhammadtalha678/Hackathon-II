# Feature Specification: Next.js Frontend with Authentication and Task Management

**Feature Branch**: `003-phase2-frontend`
**Created**: 2026-01-08
**Status**: Draft
**Input**: User description: "
Project Create:
create Next.js 16+ (App Router) project name frontend inside the phase-2 folder with tailwindcss and typescript, Documentation: (Nextjs 16 app router documentation)[https://nextjs.org/docs]

UI Create:
after create the nextjs 16 app router project now create the pages login, register, profile, a task page on which user can create task, update task, read task and delete task also mark the task as completed, Use tailwindcss, shadcn library (shadcn with nextjs app router)[https://ui.shadcn.com/docs/installation/next] for shared components (reusable component).the project must be responsive for all devices, and the UI/UX must be eye catching use the unique colors combinations
Input Fields for task is:
title,description,is_completed(checkbox (true ,false))

Better Auth Integration:
Integrate the better auth (better auth with nextjs approuter)[https://www.better-auth.com/docs/integrations/next] with Nextjs project created above. Read tehe documentation of better auth and apply the authentication:

Register with name , email and password ,confirm password
login with email and password
After user login generate the jwt token from secret key in .env file name:BETTER_AUTH_SECRET which will only available on ssr component not client side. when user login than before sending them to dashboard(show all tasks) first send the api request for all tasks of that user with the bearer jwt token in the header that i mention below route

Same happen when user refesh the page from any where in the website than check from better auth server that the token is expired or not. if token is expired check from nextjs project from server side than logout the user before sending the request to backend(fastapi)

Profile Section user can update their name
User can update password by giving the old password if user not give old password than user not able to update the password
user can not update their email because we dont have the verify email process here

neon db connection url in the .env file name DATABASE_URL in nextjs project
table create by default from better auth like example user session etc (serach in the better auth documentation) user table like (name,email,password,is_active(bool))

SENDING THE REQUEST from Nextjs Project TO BACKEND Project FASTAPI FLOW:
inside the .env file the backend url for development is:
http://127.0.0.1:8000
for production leave empty

make the AppRoutes file where all routes are stored
(user_id depends on user which user are login currently)
1)/api/{user_id}/tasks (GET all tasks)
2)/api/{user_id}/tasks/{task_id} (GET task by task_id)
3)/api/{user_id}/tasks (POST add task)
4)/api/{user_id}/tasks/{task_id} (PUT update task by task_id)
5)/api/{user_id}/tasks/{task_id} (DELETE delete task by task_id)
6)/api/{user_id}/tasks/{task_id}/complete (PATCH Toogle task as completed by task_id)

The api routes response are as follows:

1. GET All task response:(send the user_id of the login user in the api url)
   [
   {
   "updated_at": "2026-01-08T07:56:27.055288",
   "created_at": "2026-01-08T07:56:27.055288",
   "id": 3,
   "is_completed": false,
   "title": "GYM",
   "description": "Weight loss",
   "user_id": 4
   }
   ]
2. GET single task response: (send the user_id of the login user and the task_id (shows all tasks on the table) in the api url)
   {
   "updated_at": "2026-01-08T07:56:27.055288",
   "created_at": "2026-01-08T07:56:27.055288",
   "id": 3,
   "is_completed": false,
   "title": "GYM",
   "description": "Weight loss",
   "user_id": 4
   }

3. Add task response: (send the user_id of the login user in the api url with the body title reuired min=1,max=500,description default None max=2000,is_completed is required and default is False, user_id of the login user and it is required)
   {
   "updated_at": "2026-01-08T14:01:38.904695",
   "created_at": "2026-01-08T14:01:38.904695",
   "id": 8,
   "is_completed": false,
   "title": "Picnics",
   "description": "Pending",
   "user_id": 4
   }

4. Update task response: (send the user_id of the login user in the api url with the body if user submit the empty field title than show the error required otherwise if user can allow to sumit the update data )
   {
   "updated_at": "2026-01-08T14:46:05.717641",
   "created_at": "2026-01-08T14:01:38.904695",
   "id": 8,
   "is_completed": false,
   "title": "Picnics",
   "description": "Pending",
   "user_id": 4
   }

5. DELETE task response (send the user_id of the login user and the task_id (shows all tasks on the table) in the api url)
   {
   "success": true,
   "message": "Task 'Picnics' deleted successfully",
   "deleted_id": 8
   }
6. PATCH taskcomplete response (send the user_id of the login user and the task_id (shows all tasks on the table) in the api url /api/{user_id}/tasks/{task_id}/complete)
   {
   "updated_at": "2026-01-08T14:52:33.056747",
   "created_at": "2026-01-08T13:50:38.383746",
   "id": 7,
   "is_completed": true,
   "title": "Picnics",
   "description": "Pending",
   "user_id": 4
   }

branch name 003-phase3-frontend"

## Technical Documentation References

### Official Documentation Links (MUST READ & FOLLOW)

1. **Next.js 16 App Router**: https://nextjs.org/docs

   - Reference for Next.js 16+ App Router architecture, routing, and server components

2. **Better Auth with Next.js App Router**: https://www.better-auth.com/docs/integrations/next

   - Official documentation for Better Auth integration with Next.js App Router
   - MUST follow this documentation for authentication implementation
   - Covers session management, JWT token generation, and server-side validation

3. **shadcn/ui with Next.js App Router**: https://ui.shadcn.com/docs/installation/next
   - Official installation and usage guide for shadcn/ui components with Next.js App Router
   - MUST follow this documentation for component installation and configuration

### Backend Architecture

The Next.js frontend is a **client application only** that communicates with a separate **FastAPI backend** running at:

- **Development**: `http://127.0.0.1:8000`
- **Production**: (leave empty in .env)

**IMPORTANT**: The FastAPI backend handles all task data operations (CRUD). The Next.js frontend:

- Manages UI/UX and user interactions
- Handles authentication via Better Auth (user sessions, JWT tokens)
- Sends HTTP requests to FastAPI backend with JWT in Authorization header
- Receives and displays task data from FastAPI responses

## User Scenarios & Testing _(mandatory)_

### User Story 1 - User Registration and Authentication (Priority: P1)

A new user wants to create an account in the task management application. They visit the registration page, provide their name, email, password, and confirm their password. After successful registration, they can log in with their email and password to access their task dashboard. The system integrates Better Auth (following https://www.better-auth.com/docs/integrations/next) for authentication and generates JWT tokens upon login for secure API communication with the FastAPI backend at http://127.0.0.1:8000. The JWT token is sent in the Authorization header for all authenticated API requests to the backend.

**Why this priority**: Account creation and authentication is the foundational requirement that enables all other functionality. Without this, users cannot access the task management features.

**Independent Test**: Can be fully tested by registering a new user, logging in, and verifying access to the application dashboard delivers core authentication functionality with JWT token generation in header and API communication setup with FastAPI backend.

**Acceptance Scenarios**:

1. **Given** a user is on the registration page, **When** they enter valid name, email, password, and confirm password, **Then** they should be registered successfully with their information stored in the Neon database via Better Auth
2. **Given** a user has registered, **When** they enter correct email and password on login page, **Then** they should be authenticated via Better Auth, receive a JWT token from BETTER_AUTH_SECRET, and be redirected to their dashboard with JWT sent in Authorization header to FastAPI backend
3. **Given** an authenticated user with valid session, **When** they refresh the page, **Then** the system should check token validity from Better Auth server-side and remain logged in if valid
4. **Given** an authenticated user with expired JWT token, **When** they refresh the page or try to access protected resources, **Then** they should be automatically logged out server-side before any FastAPI backend requests are made

---

### User Story 2 - Comprehensive Task Management (Priority: P1)

An authenticated user wants to manage their tasks efficiently. They can create new tasks with title and description, view all their tasks on the dashboard, update existing tasks, mark tasks as completed, and delete tasks they no longer need. The Next.js application sends HTTP requests to the FastAPI backend (http://127.0.0.1:8000) to perform these operations using JWT authentication sent in the Authorization header. All API requests are made through a centralized AppRoutes file. The FastAPI backend handles all task data storage, retrieval, and modifications.

**Why this priority**: This is the core functionality of the task management application that provides primary value to users. All CRUD operations must work seamlessly with proper API integration between Next.js frontend and FastAPI backend.

**Independent Test**: Can be fully tested by performing all CRUD operations (create, read, update, delete) on tasks and verifying they work correctly with the FastAPI backend API through JWT-authenticated requests in header.

**Acceptance Scenarios**:

1. **Given** an authenticated user is on the task dashboard, **When** they click "Add Task" and fill in title (required, 1-500 chars) and optional description (up to 2000 chars), **Then** the Next.js frontend should send POST request to FastAPI backend at http://127.0.0.1:8000/api/{user_id}/tasks with JWT in header and display the newly created task returned from backend with is_completed defaulting to false
2. **Given** an authenticated user has tasks, **When** they view their dashboard, **Then** the Next.js frontend should fetch all tasks via GET request to http://127.0.0.1:8000/api/{user_id}/tasks with JWT in header and display title, description, and completion status from FastAPI backend response
3. **Given** an authenticated user wants to update a task, **When** they edit the task details and save with empty title, **Then** the system should show required error; otherwise the Next.js frontend should send PUT request to http://127.0.0.1:8000/api/{user_id}/tasks/{task_id} with JWT in header and display updated task from FastAPI backend
4. **Given** an authenticated user wants to mark a task as completed, **When** they toggle the completion checkbox, **Then** the Next.js frontend should send PATCH request to http://127.0.0.1:8000/api/{user_id}/tasks/{task_id}/complete with JWT in header and update UI with toggled status from FastAPI backend
5. **Given** an authenticated user wants to delete a task, **When** they click delete with confirmation, **Then** the Next.js frontend should send DELETE request to http://127.0.0.1:8000/api/{user_id}/tasks/{task_id} with JWT in header and show success message with deleted task name returned from FastAPI backend

---

### User Story 3 - Profile Management and Security (Priority: P2)

An authenticated user wants to update their profile information and manage their account security through Better Auth integration. They can update their name, change their password by providing their old password for verification, but cannot update their email without a verification process.

**Why this priority**: Profile management enhances user experience by allowing personalization and security management, though not essential for core task functionality.

**Independent Test**: Can be fully tested by updating user profile information and changing passwords with proper old password verification via Better Auth, ensuring changes persist across sessions in Neon database.

**Acceptance Scenarios**:

1. **Given** an authenticated user is on their profile page, **When** they update their name and save, **Then** their name should be updated in the Neon database user table via Better Auth
2. **Given** an authenticated user wants to change password, **When** they enter correct old password and new password twice, **Then** their password should be updated in the system via Better Auth
3. **Given** an authenticated user attempts to change password, **When** they do not provide old password or enter incorrect old password, **Then** the password change should be denied by Better Auth with appropriate error message
4. **Given** an authenticated user attempts to update their email, **When** they try to change the email field, **Then** the system should prevent this action with notification about lack of email verification process

---

### User Story 4 - Responsive UI with Modern Components (Priority: P2)

Users want to access the task management application on various devices with a modern, attractive interface. The application should use TailwindCSS and shadcn/ui components (following https://ui.shadcn.com/docs/installation/next) to create a responsive, visually appealing UI with unique color combinations that works well on mobile, tablet, and desktop devices.

**Why this priority**: User experience and accessibility are important for adoption and continued use of the application across different devices and screen sizes.

**Independent Test**: Can be fully tested by verifying the application layout and functionality on different screen sizes and devices, ensuring all shadcn/ui components are accessible and visually appealing.

**Acceptance Scenarios**:

1. **Given** a user accesses the application on a mobile device, **When** they interact with the shadcn/ui components, **Then** all components should be properly sized and spaced for touch interaction
2. **Given** a user accesses the application on a desktop device, **When** they interact with the shadcn/ui components, **Then** all components should be properly sized and spaced for mouse interaction
3. **Given** a user views the application, **When** they look at the interface, **Then** they should see an eye-catching, modern design with unique color combinations using TailwindCSS and shadcn/ui components
4. **Given** a user navigates between pages, **When** they use the application, **Then** the responsive design should adapt seamlessly to their screen size with consistent shadcn/ui component behavior

---

### Edge Cases

- What happens when a user tries to access another user's tasks through direct URL manipulation? The FastAPI backend should prevent unauthorized access based on user ID validation and JWT verification.
- How does the system handle network errors when communicating with the FastAPI backend API? The Next.js frontend should display appropriate error messages and allow retry mechanisms.
- What happens when a user tries to create a task with an empty title? The Next.js frontend should validate input client-side and show an error message requiring a title (min 1 character) before sending to FastAPI backend.
- What happens when a user tries to create a task with title exceeding 500 characters? The Next.js frontend should validate and prevent submission with appropriate error message before sending to FastAPI backend.
- What happens when a user tries to create a task with description exceeding 2000 characters? The Next.js frontend should validate and prevent submission with appropriate error message before sending to FastAPI backend.
- How does the system handle concurrent updates to the same task by the same user? The FastAPI backend should handle updates sequentially with appropriate feedback returned to Next.js frontend.
- What happens when the FastAPI backend at http://127.0.0.1:8000 is temporarily unavailable? The Next.js frontend should gracefully handle errors and notify users without crashing.
- What happens when JWT token expires during a task operation? The Next.js frontend should detect token expiration on page refresh via Better Auth server-side check and redirect to login before making any FastAPI backend operations.
- What happens when user refreshes the page during task creation? The Next.js frontend should check JWT validity server-side via Better Auth and maintain session if token is valid.

## Requirements _(mandatory)_

### Functional Requirements

#### Authentication & Authorization (Better Auth Integration)

- **FR-001**: System MUST integrate Better Auth following official documentation at https://www.better-auth.com/docs/integrations/next for all authentication functionality
- **FR-002**: System MUST allow users to register with name, email, password, and password confirmation using Better Auth
- **FR-003**: System MUST authenticate users via email and password using Better Auth integration with JWT token generation
- **FR-004**: System MUST generate JWT tokens from BETTER_AUTH_SECRET (stored in .env file, only available on SSR components, not client-side) upon successful authentication
- **FR-005**: System MUST send JWT tokens in the Authorization header (Bearer token) for all authenticated API requests to FastAPI backend at http://127.0.0.1:8000
- **FR-006**: System MUST validate JWT tokens on page refresh by checking with Better Auth server from server-side and automatically log out users if tokens are expired before making any FastAPI backend requests
- **FR-007**: System MUST redirect authenticated users to dashboard after login, which first sends GET request to http://127.0.0.1:8000/api/{user_id}/tasks with JWT in header
- **FR-008**: System MUST connect to Neon database using DATABASE_URL from environment variables for Better Auth tables (users, sessions, etc.)
- **FR-009**: System MUST create default Better Auth tables automatically including user table with fields: name, email, password, is_active (boolean)

#### Task Management (Communication with FastAPI Backend)

- **FR-010**: System MUST implement centralized AppRoutes file where all FastAPI backend API routes are stored and managed
- **FR-011**: System MUST send all task-related HTTP requests to FastAPI backend at http://127.0.0.1:8000 (development) with JWT in Authorization header
- **FR-012**: Users MUST be able to create tasks by sending POST request to http://127.0.0.1:8000/api/{user_id}/tasks with title (required, min 1, max 500 characters), description (optional, default None, max 2000 characters), is_completed (default false), and user_id in request body
- **FR-013**: Users MUST be able to view all their tasks on dashboard by sending GET request to http://127.0.0.1:8000/api/{user_id}/tasks with JWT in header, receiving array of task objects from FastAPI backend
- **FR-014**: Users MUST be able to view a single task by sending GET request to http://127.0.0.1:8000/api/{user_id}/tasks/{task_id} with JWT in header, receiving task object from FastAPI backend
- **FR-015**: Users MUST be able to update existing tasks by sending PUT request to http://127.0.0.1:8000/api/{user_id}/tasks/{task_id} with JWT in header and updated task data to FastAPI backend
- **FR-016**: System MUST validate that title is not empty during task update on Next.js frontend and show required error if empty before sending to FastAPI backend
- **FR-017**: Users MUST be able to delete tasks by sending DELETE request to http://127.0.0.1:8000/api/{user_id}/tasks/{task_id} with JWT in header and receive success confirmation from FastAPI backend
- **FR-018**: Users MUST be able to toggle task completion status by sending PATCH request to http://127.0.0.1:8000/api/{user_id}/tasks/{task_id}/complete with JWT in header, receiving updated task from FastAPI backend
- **FR-019**: System MUST handle all task data operations (create, read, update, delete) through FastAPI backend, with Next.js frontend only managing UI/UX and HTTP requests

#### Profile Management (Better Auth)

- **FR-020**: Users MUST be able to update their profile name via Better Auth user management functionality
- **FR-021**: Users MUST be able to change their password only by providing old password for verification through Better Auth
- **FR-022**: System MUST NOT allow users to change password if old password is not provided or is incorrect, validated by Better Auth
- **FR-023**: System MUST NOT allow users to update their email address due to lack of email verification process

#### UI/UX Requirements (shadcn/ui + TailwindCSS)

- **FR-024**: System MUST integrate shadcn/ui library following official documentation at https://ui.shadcn.com/docs/installation/next for all reusable UI components
- **FR-025**: System MUST create pages for: login, register, profile, and task management (create, read, update, delete tasks, mark as completed)
- **FR-026**: System MUST be responsive and work on all device sizes (mobile, tablet, desktop) using TailwindCSS
- **FR-027**: System MUST implement eye-catching UI/UX with unique color combinations using TailwindCSS
- **FR-028**: System MUST use shadcn/ui components for consistent, reusable UI elements throughout the application
- **FR-029**: System MUST use proper error handling and display user-friendly messages for API failures from FastAPI backend

#### Environment & Configuration

- **FR-030**: System MUST store BETTER_AUTH_SECRET in .env file (only available on SSR components, not client-side) for JWT generation and validation
- **FR-031**: System MUST store DATABASE_URL in .env file for Neon database connection used by Better Auth
- **FR-032**: System MUST store backend URL in .env file as http://127.0.0.1:8000 for development, empty for production
- **FR-033**: System MUST send user_id of currently logged-in user in all FastAPI backend API URL paths
- **FR-034**: System MUST implement proper session validation on every page load/refresh to check JWT token validity from Better Auth server on server-side

### Key Entities

- **User**: Represents a registered user in Neon database via Better Auth with attributes: id, name (string), email (string, unique), password (hashed string), is_active (boolean), creation timestamp, update timestamp
- **Task**: Represents a user's task stored in FastAPI backend database with attributes: id (integer), title (string, required, min 1 char, max 500 chars), description (string, optional, default None, max 2000 chars), is_completed (boolean, default false), user_id (integer, foreign key), created_at (timestamp), updated_at (timestamp)
- **Session**: Represents an authenticated user session managed by Better Auth with JWT token, user ID, expiration time, creation timestamp
- **Authentication Token**: Represents the JWT generated using BETTER_AUTH_SECRET containing user identity and expiration information, sent in Authorization header as Bearer token to FastAPI backend

### Environment Variables (.env file)

- **DATABASE_URL**: Neon database connection URL for Better Auth tables (users, sessions, etc.)
- **BETTER_AUTH_SECRET**: Secret key for JWT token generation and validation (only available on SSR components, not client-side)
- **BACKEND_URL**: FastAPI backend API base URL
  - Development: `http://127.0.0.1:8000`
  - Production: (leave empty)

### API Routes Structure (AppRoutes File)

All backend API routes communicate with FastAPI backend at http://127.0.0.1:8000, use the currently logged-in user's user_id, and send JWT token in Authorization header:

1. **GET http://127.0.0.1:8000/api/{user_id}/tasks** - Retrieve all tasks for the logged-in user from FastAPI backend
2. **GET http://127.0.0.1:8000/api/{user_id}/tasks/{task_id}** - Retrieve a single task by task_id from FastAPI backend
3. **POST http://127.0.0.1:8000/api/{user_id}/tasks** - Create a new task on FastAPI backend (body includes: title, description, is_completed default false, user_id)
4. **PUT http://127.0.0.1:8000/api/{user_id}/tasks/{task_id}** - Update an existing task by task_id on FastAPI backend
5. **DELETE http://127.0.0.1:8000/api/{user_id}/tasks/{task_id}** - Delete a task by task_id on FastAPI backend
6. **PATCH http://127.0.0.1:8000/api/{user_id}/tasks/{task_id}/complete** - Toggle task completion status on FastAPI backend

### API Response Formats (from FastAPI Backend)

All responses below are returned by the FastAPI backend at http://127.0.0.1:8000:

**GET All Tasks Response:**

```json
[
  {
    "updated_at": "2026-01-08T07:56:27.055288",
    "created_at": "2026-01-08T07:56:27.055288",
    "id": 3,
    "is_completed": false,
    "title": "GYM",
    "description": "Weight loss",
    "user_id": 4
  }
]
```

**GET Single Task Response:**

```json
{
  "updated_at": "2026-01-08T07:56:27.055288",
  "created_at": "2026-01-08T07:56:27.055288",
  "id": 3,
  "is_completed": false,
  "title": "GYM",
  "description": "Weight loss",
  "user_id": 4
}
```

**POST Add Task Response:**

```json
{
  "updated_at": "2026-01-08T14:01:38.904695",
  "created_at": "2026-01-08T14:01:38.904695",
  "id": 8,
  "is_completed": false,
  "title": "Picnics",
  "description": "Pending",
  "user_id": 4
}
```

**PUT Update Task Response:**

```json
{
  "updated_at": "2026-01-08T14:46:05.717641",
  "created_at": "2026-01-08T14:01:38.904695",
  "id": 8,
  "is_completed": false,
  "title": "Picnics",
  "description": "Pending",
  "user_id": 4
}
```

**DELETE Task Response:**

```json
{
  "success": true,
  "message": "Task 'Picnics' deleted successfully",
  "deleted_id": 8
}
```

**PATCH Toggle Complete Response:**

```json
{
  "updated_at": "2026-01-08T14:52:33.056747",
  "created_at": "2026-01-08T13:50:38.383746",
  "id": 7,
  "is_completed": true,
  "title": "Picnics",
  "description": "Pending",
  "user_id": 4
}
```

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Better Auth integration following https://www.better-auth.com/docs/integrations/next is implemented correctly with 100% authentication success rate
- **SC-002**: shadcn/ui integration following https://ui.shadcn.com/docs/installation/next is implemented correctly with all components working on all devices
- **SC-003**: Users can register and log in within 30 seconds on average with successful JWT token generation and storage in Authorization header
- **SC-004**: Users can create, read, update, and delete tasks with 99% success rate through FastAPI backend API communication at http://127.0.0.1:8000 with JWT in header
- **SC-005**: 95% of users can complete the primary task management workflow (create, update, complete, delete tasks) without assistance using the eye-catching UI with shadcn/ui components
- **SC-006**: Application loads and responds to user actions within 2 seconds on average including API calls to FastAPI backend with JWT authentication
- **SC-007**: System properly handles authentication via Better Auth and prevents unauthorized access to user data 100% of the time through JWT validation
- **SC-008**: Application is usable on mobile, tablet, and desktop devices with consistent, responsive experience using TailwindCSS and shadcn/ui components
- **SC-009**: All specified API endpoints at http://127.0.0.1:8000 return responses in the exact format specified in the requirements from FastAPI backend
- **SC-010**: Password change functionality via Better Auth works correctly with old password verification 100% of the time
- **SC-011**: JWT token expiration is detected 100% of the time on page refresh via Better Auth server-side check with automatic logout before FastAPI backend requests
- **SC-012**: All API requests include JWT token in Authorization header 100% of the time for authenticated operations to FastAPI backend
- **SC-013**: Task creation with default is_completed=false works 100% of the time without requiring explicit value when sent to FastAPI backend
- **SC-014**: Title validation (min 1, max 500 chars) and description validation (max 2000 chars) work 100% of the time before sending to FastAPI backend
- **SC-015**: AppRoutes file successfully centralizes all FastAPI backend API route definitions at http://127.0.0.1:8000
- **SC-016**: Next.js frontend successfully communicates with FastAPI backend for all task operations with proper error handling and user feedback
