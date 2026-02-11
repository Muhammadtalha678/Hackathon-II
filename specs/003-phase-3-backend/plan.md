# Implementation Plan: Backend of Todo AI Chatbot (Phase-3)

**Feature**: 003-phase-3-backend  
**Created**: 2026-02-12  
**Status**: Draft

## Technical Context

The implementation will extend the existing backend to support an AI chatbot that can manage tasks through natural language. The system will use OpenAI's Agent SDK to process user requests and invoke MCP tools for task operations. The architecture will be stateless, with all conversation data persisted to the database.

### Technologies & Dependencies

- **FastAPI**: Web framework for creating the API endpoints
- **OpenAI SDK**: For implementing the AI agent functionality
- **SQLAlchemy/asyncpg**: For database operations (assuming PostgreSQL)
- **MCP SDK**: For implementing stateless tools
- **Pydantic**: For data validation
- **JWT**: For authentication and authorization

### Known Unknowns

- Specific database schema for existing backend (NEEDS CLARIFICATION)
- Current authentication mechanism in existing backend (NEEDS CLARIFICATION)
- MCP server configuration and endpoint details (NEEDS CLARIFICATION)
- OpenAI model selection and configuration parameters (NEEDS CLARIFICATION)

## Constitution Check

### Spec-Driven Development
- All implementation will follow the specifications defined in spec.md
- Code will be generated based on API contracts and data models defined in this plan

### Clean Code
- Follow Python conventions (PEP 8)
- Use type hints for all function parameters and return values
- Write comprehensive docstrings for all public functions

### Test-First Development
- Write tests for each component before implementation
- Include unit tests for MCP tools, integration tests for API endpoints
- Test error handling and edge cases

### Single Responsibility
- Separate concerns: API layer, business logic, data access, and MCP tools
- Each module will have a single, well-defined purpose

### Evolutionary Architecture
- Design for extensibility and maintainability
- Ensure the architecture supports future enhancements

### User Experience First
- Provide clear error messages
- Ensure responsive API responses

## Gates

### Gate 1: Architecture Feasibility
✅ The architecture is technically feasible with the selected technologies.

### Gate 2: Dependency Availability
✅ All required dependencies (OpenAI SDK, FastAPI, MCP SDK) are available.

### Gate 3: Compliance with Constitution
✅ The plan aligns with all constitutional principles.

## Phase 0: Research & Resolution of Unknowns

### Research Tasks

#### RT-001: Existing Backend Architecture Investigation
**Task**: Investigate the current backend structure and database schema
**Rationale**: Understanding the existing architecture is essential for extending it properly
**Outcome**: Documentation of current database schema and API structure
**Status**: COMPLETED - See research.md for details

#### RT-002: Authentication Mechanism Analysis
**Task**: Determine how user authentication is currently handled
**Rationale**: Need to ensure the new chat endpoint integrates properly with existing auth
**Outcome**: Clear understanding of JWT token handling or other auth mechanism
**Status**: COMPLETED - See research.md for details

#### RT-003: MCP Server Setup
**Task**: Set up and configure the MCP server for stateless tools
**Rationale**: MCP tools are essential for the AI agent to perform task operations
**Outcome**: Running MCP server with endpoints for task operations
**Status**: COMPLETED - See research.md for details

#### RT-004: OpenAI Agent Configuration
**Task**: Configure OpenAI Agent SDK for the chatbot functionality
**Rationale**: The agent needs to be properly configured to understand user intent and call MCP tools
**Outcome**: Working OpenAI agent that can process natural language and invoke tools
**Status**: COMPLETED - See research.md for details

## Phase 1: Data Model & API Design

### Data Models

#### Conversation Model
```
Conversation:
- id: UUID (primary key)
- user_id: UUID (foreign key to user)
- created_at: DateTime (timestamp)
- updated_at: DateTime (timestamp)
```

#### Message Model
```
Message:
- id: UUID (primary key)
- user_id: UUID (foreign key to user)
- conversation_id: UUID (foreign key to conversation)
- role: String (enum: 'user' | 'assistant')
- content: Text (the message content)
- created_at: DateTime (timestamp)
```

### API Contracts

#### POST /api/{user_id}/chat
**Description**: Endpoint for users to interact with the AI assistant
**Authentication**: JWT token required
**Request Body**:
```json
{
  "message": "string",
  "conversation_id": "optional UUID"
}
```
**Response**:
```json
{
  "response": "string",
  "conversation_id": "UUID",
  "timestamp": "ISO 8601 datetime"
}
```

#### Error Responses
All endpoints return appropriate HTTP status codes:
- 200: Success
- 400: Bad Request (malformed input)
- 401: Unauthorized (invalid JWT)
- 403: Forbidden (user doesn't have access to resource)
- 404: Not Found (resource doesn't exist)
- 500: Internal Server Error

### MCP Tools API

#### add_task(user_id: str, task_data: dict) -> dict
**Description**: Adds a new task to the user's task list
**Parameters**: 
- user_id: The ID of the user
- task_data: Object containing task details
**Returns**: Structured JSON with task creation result

#### list_tasks(user_id: str, filters: dict = None) -> dict
**Description**: Lists tasks for the user
**Parameters**:
- user_id: The ID of the user
- filters: Optional object with filtering criteria
**Returns**: Structured JSON with list of tasks

#### complete_task(user_id: str, task_id: str) -> dict
**Description**: Marks a task as completed
**Parameters**:
- user_id: The ID of the user
- task_id: The ID of the task to complete
**Returns**: Structured JSON with completion result

#### delete_task(user_id: str, task_id: str) -> dict
**Description**: Deletes a task from the user's list
**Parameters**:
- user_id: The ID of the user
- task_id: The ID of the task to delete
**Returns**: Structured JSON with deletion result

#### update_task(user_id: str, task_id: str, updates: dict) -> dict
**Description**: Updates task details
**Parameters**:
- user_id: The ID of the user
- task_id: The ID of the task to update
- updates: Object containing fields to update
**Returns**: Structured JSON with update result

**Status**: COMPLETED - See data-model.md and contracts/chat-api.yaml for details

## Phase 2: Implementation Plan

### Phase 2.1: MCP Tools Implementation
**Objective**: Implement stateless HTTP tools for task operations
- Implement add_task, list_tasks, complete_task, delete_task, update_task endpoints
- Ensure each tool accepts user_id explicitly
- Ensure each tool performs DB operations
- Ensure each tool returns structured JSON

### Phase 2.2: Database Layer Enhancement
**Objective**: Extend the database to support conversations and messages
- Create Conversation and Message table schemas
- Implement SQLAlchemy models
- Implement data access layer functions

### Phase 2.3: OpenAI Agent Integration
**Objective**: Integrate OpenAI Agent SDK with MCP tools
- Configure OpenAI Agent with appropriate tools
- Implement natural language processing
- Implement tool calling logic

### Phase 2.4: Chat API Endpoint
**Objective**: Implement the main chat endpoint
- Create POST /api/{user_id}/chat endpoint
- Implement conversation history retrieval
- Implement message storage
- Connect to OpenAI Agent
- Return AI response to client

### Phase 2.5: Statelessness Verification
**Objective**: Ensure the server maintains no in-memory state
- Verify all data is persisted to DB
- Test stateless behavior across requests
- Implement proper session management through DB

## Phase 3: Validation & Testing

### VT-001: Statelessness Verification
**Test**: Verify that the server maintains no in-memory state between requests
**Method**: Restart server between requests and verify functionality remains intact

### VT-002: Tool Chaining Test
**Test**: Verify that the AI agent can chain multiple MCP tool calls in a single interaction
**Method**: Simulate complex user requests that require multiple tool calls

### VT-003: Conversation Resumption Test
**Test**: Verify that conversation history is properly maintained and resumed
**Method**: Initiate conversation, make requests, then simulate new request with same conversation_id

### VT-004: Error Handling Test
**Test**: Verify graceful error handling in all components
**Method**: Simulate various error conditions and verify appropriate responses

## Quickstart Guide

### Prerequisites
- Python 3.9+
- OpenAI API key
- MCP server running
- Database connection

### Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables:
   - OPENAI_API_KEY
   - DATABASE_URL
   - MCP_SERVER_ENDPOINT
   - JWT_SECRET
3. Run database migrations: `alembic upgrade head`
4. Start the server: `uvicorn main:app --reload`

### Running Tests
- Unit tests: `pytest tests/unit/`
- Integration tests: `pytest tests/integration/`
- End-to-end tests: `pytest tests/e2e/`

## Agent Context Update

The following technologies are being added to the agent context:
- OpenAI Agent SDK
- MCP (Model Context Protocol) tools
- Conversation and Message data models
- FastAPI endpoint patterns for chat functionality