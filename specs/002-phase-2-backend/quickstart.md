# Quickstart Guide: JWT Task Management API

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Virtual environment tool (recommended: `venv` or `uv`)

## Setup Instructions

### 1. Clone or Create Project

```bash
# If using uv (recommended)
uv init backend
cd backend

# Or create a new directory
mkdir backend && cd backend
```

### 2. Create Virtual Environment

```bash
# Using uv (recommended)
uv venv

# Or using standard venv
python -m venv .venv
```

### 3. Activate Virtual Environment

```bash
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
# Using uv (recommended)
uv add "fastapi>=0.100.0" "uvicorn[standard]" "sqlmodel" "python-dotenv" "pyjwt" "psycopg2-binary"

# Or using pip
pip install "fastapi>=0.100.0" "uvicorn[standard]" "sqlmodel" "python-dotenv" "pyjwt" "psycopg2-binary"
```

### 5. Create Project Structure

```bash
mkdir -p src/{models,controllers,routers,lib} tests
```

### 6. Environment Configuration

Create `.env` file with the following content:

```env
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
DATABASE_URL=sqlite:///./task_management.db
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Also create `.env.example`:

```env
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
DATABASE_URL=sqlite:///./task_management.db
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 7. Run the Application

```bash
# Start the development server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## API Usage

### Authentication

All API endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

### Example Requests

```bash
# List user's tasks
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/{user_id}/tasks

# Create a new task
curl -X POST -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"title": "New Task", "description": "Task description"}' \
     http://localhost:8000/api/{user_id}/tasks
```

## Testing

Run the tests using pytest:

```bash
pytest tests/ -v
```
