# Research Summary: Backend of Todo AI Chatbot (Phase-3)

## Overview
This document summarizes research conducted to resolve unknowns and make key decisions for implementing the AI chatbot backend.

## Decision: Database Schema Integration
**Rationale**: Need to understand existing database structure to properly extend it with Conversation and Message tables.
**Approach**: Since we don't have access to the current schema, we'll implement using a common pattern that can be adapted to the existing structure. We'll use UUIDs for primary keys and foreign keys to maintain consistency with typical modern applications.

**Alternatives considered**:
- Using integer IDs: Less secure and predictable
- Separate database: More complex but isolated
- In-memory storage: Violates the statelessness requirement

## Decision: Authentication Method
**Rationale**: Need to integrate with existing authentication system to ensure user_id is properly validated.
**Approach**: Assuming JWT-based authentication based on the requirement to accept user_id explicitly. We'll implement middleware to validate JWT tokens and extract user_id from the token claims.

**Alternatives considered**:
- Session-based authentication: Would require storing state
- API keys: Less secure for user-specific operations
- OAuth: Overly complex for this use case

## Decision: MCP Server Configuration
**Rationale**: MCP tools need to be accessible to the OpenAI agent for task operations.
**Approach**: MCP tools will be implemented as HTTP endpoints that the agent can call. These will be registered with the OpenAI agent as available functions.

**Alternatives considered**:
- Direct database access from agent: Would violate statelessness
- WebSocket connections: More complex than needed
- gRPC services: Overly complex for this use case

## Decision: OpenAI Model Selection
**Rationale**: Need to select an appropriate model that can effectively interpret natural language and call tools.
**Approach**: Using GPT-4 or GPT-4 Turbo as it has strong function calling capabilities and can effectively interpret natural language to call the appropriate MCP tools.

**Alternatives considered**:
- GPT-3.5: Less capable but faster and cheaper
- Custom models: More complex to train and maintain
- Other providers: Would complicate the architecture

## Decision: Conversation Storage Strategy
**Rationale**: Need to efficiently store and retrieve conversation history while maintaining performance.
**Approach**: Storing conversations and messages in separate tables with proper indexing on user_id and conversation_id to enable efficient retrieval.

**Alternatives considered**:
- Storing as JSON blobs: Less queryable
- Separate database per user: More complex management
- In-memory caching: Violates statelessness requirement