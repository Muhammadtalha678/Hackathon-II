---
id: 001
title: create-specification
stage: spec
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase3-frontend
branch: 003-phase3-frontend
user: Muhammad Talha
command: /sp.specify
labels: ["frontend", "authentication", "task-management", "specification"]
links:
  spec: E:/Hackathons/Hackathon-II/specs/003-phase3-frontend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - E:/Hackathons/Hackathon-II/specs/003-phase3-frontend/spec.md
  - E:/Hackathons/Hackathon-II/specs/003-phase3-frontend/checklists/requirements.md
tests:
  - spec validation completed
---

## Prompt

```
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
After user login generate the jwt token from secret key in .env file name:BETTER_AUTH_SECRET which will only available on ssr component not client side. when user login than before sending them to dashboard(show all tasks) first send the api request for all tasks of that user with the bearer jwt token in the cookie or header (your choice) that i mention below route

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
1) GET All task response:(send the user_id of the login user in the api url)
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
2) GET single task response: (send the user_id of the login user and the task_id (shows all tasks on the table) in the api url)
    {
        "updated_at": "2026-01-08T07:56:27.055288",
        "created_at": "2026-01-08T07:56:27.055288",
        "id": 3,
        "is_completed": false,
        "title": "GYM",
        "description": "Weight loss",
        "user_id": 4
    }

3) Add task response: (send the user_id of the login user in the api url with the body title reuired min=1,max=500,description default None max=2000,is_completed is required and default is False, user_id of the login user and it is required)
    {
    "updated_at": "2026-01-08T14:01:38.904695",
    "created_at": "2026-01-08T14:01:38.904695",
    "id": 8,
    "is_completed": false,
    "title": "Picnics",
    "description": "Pending",
    "user_id": 4
    }

4) Update task response: (send the user_id of the login user in the api url with the body if user submit the empty field title  than show the error required  otherwise if user can allow to sumit the update data )
    {
        "updated_at": "2026-01-08T14:46:05.717641",
        "created_at": "2026-01-08T14:01:38.904695",
        "id": 8,
        "is_completed": false,
        "title": "Picnics",
        "description": "Pending",
        "user_id": 4
    }

5) DELETE task response (send the user_id of the login user and the task_id (shows all tasks on the table) in the api url)
    {
  "success": true,
  "message": "Task 'Picnics' deleted successfully",
  "deleted_id": 8
}
6) PATCH taskcomplete response (send the user_id of the login user and the task_id (shows all tasks on the table) in the api url /api/{user_id}/tasks/{task_id}/complete)
    {
  "updated_at": "2026-01-08T14:52:33.056747",
  "created_at": "2026-01-08T13:50:38.383746",
  "id": 7,
  "is_completed": true,
  "title": "Picnics",
  "description": "Pending",
  "user_id": 4
}

branch name 003-phase2-frontend
```

## Response snapshot

Created a comprehensive specification for the Next.js frontend with authentication and task management. The specification includes:

- User Scenarios & Testing with 4 prioritized user stories covering registration/login, task management, profile management, and session security
- Functional Requirements (23 specific requirements covering authentication, task operations, security, and responsiveness)
- Key Entities (User, Task, Session, and Authentication Token definitions)
- Success Criteria (8 measurable outcomes)

Also created a quality checklist to validate the specification completeness.

## Outcome

- ✅ Impact: Created complete feature specification for Next.js frontend with authentication and task management
- 🧪 Tests: spec validation completed
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: Specification covers all requirements from user description with clear acceptance criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
