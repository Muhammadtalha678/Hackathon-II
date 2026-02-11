# Quickstart Guide: Backend of Todo AI Chatbot (Phase-3)

## Overview
This guide provides instructions for setting up, running, and testing the AI chatbot backend.

## Prerequisites
- Python 3.9 or higher
- pip package manager
- Access to OpenAI API (valid API key)
- PostgreSQL database (or compatible)
- MCP server running with task endpoints

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot_db
MCP_SERVER_ENDPOINT=https://your-mcp-server.com/api
JWT_SECRET=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Setup

### 1. Run Migrations
```bash
alembic upgrade head
```

### 2. Seed Initial Data (Optional)
```bash
python scripts/seed_db.py
```

## Running the Application

### 1. Start the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Alternative: Using Gunicorn (Production)
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Usage

### 1. Send a Message to the AI Assistant
```bash
curl -X POST \
  http://localhost:8000/api/{user_id}/chat \
  -H 'Authorization: Bearer {jwt_token}' \
  -H 'Content-Type: application/json' \
  -d '{"message": "Add a task to buy groceries"}'
```

### 2. Continue an Existing Conversation
```bash
curl -X POST \
  http://localhost:8000/api/{user_id}/chat \
  -H 'Authorization: Bearer {jwt_token}' \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Mark the grocery task as completed",
    "conversation_id": "{existing_conversation_id}"
  }'
```

## Testing

### 1. Run Unit Tests
```bash
pytest tests/unit/
```

### 2. Run Integration Tests
```bash
pytest tests/integration/
```

### 3. Run All Tests
```bash
pytest
```

### 4. Run Tests with Coverage
```bash
pytest --cov=src/ --cov-report=html
```

## MCP Tools Configuration

The AI agent uses MCP (Model Context Protocol) tools to perform task operations. These tools are configured in the agent initialization:

- `add_task`: Creates new tasks
- `list_tasks`: Retrieves user's tasks
- `complete_task`: Marks tasks as completed
- `delete_task`: Removes tasks
- `update_task`: Modifies existing tasks

Each tool accepts a `user_id` parameter to ensure proper user isolation.

## Troubleshooting

### Common Issues

1. **OpenAI API Connection Error**
   - Verify your API key is correct
   - Check internet connectivity
   - Ensure you have sufficient quota

2. **Database Connection Error**
   - Verify database credentials in `.env`
   - Check that the database server is running
   - Ensure the database exists

3. **JWT Authentication Error**
   - Verify JWT token is valid and not expired
   - Check that the secret key matches between services

4. **MCP Tools Unavailable**
   - Verify MCP server is running
   - Check that endpoints are accessible
   - Confirm authentication with MCP server

### Enable Debug Logging
Set the LOG_LEVEL environment variable to "DEBUG":
```bash
LOG_LEVEL=DEBUG uvicorn main:app --reload
```

## Development

### Adding New MCP Tools
1. Define the new tool function in the MCP tools module
2. Register the tool with the OpenAI agent
3. Add appropriate validation and error handling
4. Write tests for the new functionality

### Extending the Data Model
1. Update the data model definition in `data-model.md`
2. Create a new Alembic migration
3. Update the SQLAlchemy models
4. Update any affected business logic
5. Write tests for the new functionality