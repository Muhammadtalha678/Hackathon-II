# Data Model: Backend of Todo AI Chatbot (Phase-3)

## Overview
This document defines the data models for the AI chatbot backend, including the Conversation and Message entities as specified in the feature requirements.

## Entity: Conversation

### Fields
- **id**: UUID (Primary Key)
  - Type: UUID (Universally Unique Identifier)
  - Constraints: Not null, unique
  - Description: Unique identifier for the conversation
  
- **user_id**: UUID (Foreign Key)
  - Type: UUID
  - Constraints: Not null, references users(id)
  - Description: Links the conversation to a specific user
  
- **created_at**: DateTime
  - Type: DateTime (with timezone)
  - Constraints: Not null, default: current timestamp
  - Description: Timestamp when the conversation was created
  
- **updated_at**: DateTime
  - Type: DateTime (with timezone)
  - Constraints: Not null, default: current timestamp
  - Description: Timestamp when the conversation was last updated

### Relationships
- One-to-many: A Conversation has many Messages
- Many-to-one: A Conversation belongs to one User

### Validation Rules
- user_id must correspond to an existing user
- created_at must be in the past or present
- updated_at must be equal to or later than created_at

## Entity: Message

### Fields
- **id**: UUID (Primary Key)
  - Type: UUID
  - Constraints: Not null, unique
  - Description: Unique identifier for the message
  
- **user_id**: UUID (Foreign Key)
  - Type: UUID
  - Constraints: Not null, references users(id)
  - Description: Links the message to a specific user (redundant with conversation but for quick lookup)
  
- **conversation_id**: UUID (Foreign Key)
  - Type: UUID
  - Constraints: Not null, references conversations(id)
  - Description: Links the message to a specific conversation
  
- **role**: String (Enum)
  - Type: String
  - Constraints: Not null, values: 'user' | 'assistant'
  - Description: Indicates whether the message was sent by the user or the assistant
  
- **content**: Text
  - Type: Text (variable length)
  - Constraints: Not null
  - Description: The actual content of the message
  
- **created_at**: DateTime
  - Type: DateTime (with timezone)
  - Constraints: Not null, default: current timestamp
  - Description: Timestamp when the message was created

### Relationships
- Many-to-one: A Message belongs to one Conversation
- Many-to-one: A Message belongs to one User

### Validation Rules
- user_id must correspond to an existing user
- conversation_id must correspond to an existing conversation
- role must be either 'user' or 'assistant'
- content must not be empty
- created_at must be in the past or present

## Entity: Task (Existing)

### Fields (Assumed from context)
- **id**: UUID (Primary Key)
  - Type: UUID
  - Constraints: Not null, unique
  - Description: Unique identifier for the task
  
- **user_id**: UUID (Foreign Key)
  - Type: UUID
  - Constraints: Not null, references users(id)
  - Description: Links the task to a specific user
  
- **title**: String
  - Type: String (variable length)
  - Constraints: Not null
  - Description: Title or brief description of the task
  
- **description**: Text
  - Type: Text (variable length)
  - Constraints: Nullable
  - Description: Detailed description of the task
  
- **status**: String (Enum)
  - Type: String
  - Constraints: Not null, values: 'pending' | 'in_progress' | 'completed'
  - Description: Current status of the task
  
- **created_at**: DateTime
  - Type: DateTime (with timezone)
  - Constraints: Not null, default: current timestamp
  - Description: Timestamp when the task was created
  
- **updated_at**: DateTime
  - Type: DateTime (with timezone)
  - Constraints: Not null, default: current timestamp
  - Description: Timestamp when the task was last updated

### Relationships
- Many-to-one: A Task belongs to one User

### Validation Rules
- user_id must correspond to an existing user
- title must not be empty
- status must be one of the allowed values
- created_at must be in the past or present
- updated_at must be equal to or later than created_at

## State Transitions

### Task Status Transitions
- From 'pending' to 'in_progress': When a user starts working on the task
- From 'in_progress' to 'completed': When a user finishes the task
- From 'completed' to 'pending': When a user reopens a completed task
- From 'in_progress' to 'pending': When a user stops working on the task

## Indexes

For optimal performance, the following indexes should be created:

1. **conversations_user_id_idx**: On conversations(user_id) for efficient user-specific queries
2. **messages_conversation_id_idx**: On messages(conversation_id) for efficient conversation history retrieval
3. **messages_user_id_idx**: On messages(user_id) for efficient user-specific queries
4. **messages_created_at_idx**: On messages(created_at) for chronological ordering
5. **tasks_user_id_idx**: On tasks(user_id) for efficient user-specific queries
6. **tasks_status_idx**: On tasks(status) for efficient status-based queries