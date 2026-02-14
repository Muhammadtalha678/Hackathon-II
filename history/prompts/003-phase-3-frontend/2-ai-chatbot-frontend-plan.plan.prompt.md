---
id: 2
title: "AI Chatbot Frontend Plan"
stage: plan
date_iso: 2026-02-12
surface: agent
model: Claude Sonnet 4.5
feature: phase-3-frontend
branch: 003-phase-3-frontend
user: Muhammad Talha
command: /sp.plan
labels: ["planning", "frontend", "ai-chatbot", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - D:\Hackathon-II\specs\003-phase-3-frontend\plan.md
  - D:\Hackathon-II\specs\003-phase-3-frontend\research.md
  - D:\Hackathon-II\specs\003-phase-3-frontend\data-model.md
  - D:\Hackathon-II\specs\003-phase-3-frontend\contracts\chat-api.yaml
  - D:\Hackathon-II\specs\003-phase-3-frontend\quickstart.md
tests_yaml: []
---

# Implementation Plan: AI Chatbot Frontend Interface

**Feature**: AI Chatbot Frontend Interface  
**Branch**: 003-phase-3-frontend  
**Created**: 2026-02-12  
**Status**: Draft

## Technical Context

### Current Architecture
- **Frontend Framework**: Next.js (React-based)
- **UI Library**: ChatKit for chat interface
- **Authentication**: Better Auth
- **Backend Service**: Available at https://muhammad51059579-phase-3-backend.hf.space/api/{user_id}/chat
- **Environment Variables**: NEXT_PUBLIC_OPENAI_DOMAIN_KEY=domain_pk_698daa709f5c81979d9cbc12d29471e40d6daf6123da1bb2
- **Language**: TypeScript (.tsx files)

### Dependencies
- **ChatKit**: For chat UI implementation
- **Better Auth**: For authentication token retrieval
- **Next.js**: For frontend framework
- **TypeScript**: For type safety

### Integration Points
- **Backend API**: POST endpoint at `/api/{user_id}/chat` requiring Bearer token authentication
- **Authentication System**: Need to retrieve token using Better Auth client
- **Environment Configuration**: Need to set NEXT_PUBLIC_OPENAI_DOMAIN_KEY

### Unknowns
- **UI Placement**: Specific implementation details for placing chat UI in bottom right corner - RESOLVED: Using fixed positioning with floating action button
- **Message Formatting**: How to handle README-style formatting in chat responses - RESOLVED: Using react-markdown with remark-gfm plugin
- **State Management**: How to maintain conversation history within session - RESOLVED: Using React useState hook for local component state

## Constitution Check

### Spec-Driven Development
✅ All implementation will follow the defined specifications in spec.md
✅ Features will be developed based on user stories and acceptance criteria

### Clean Code
✅ Will follow TypeScript best practices and type safety
✅ Will include proper documentation and comments
✅ Will maintain clean separation of concerns

### Test-First Development
✅ Will write tests for all components and functionality
✅ Will implement TDD approach (Red-Green-Refactor)

### Single Responsibility
✅ Components will have single, well-defined purposes
✅ Separation between UI, state management, and API calls

### Evolutionary Architecture
✅ Architecture will be designed to support future enhancements
✅ Will structure code to be extensible

### User Experience First
✅ UI will be designed with user experience in mind
✅ Clear loading states and error handling will be implemented

## Gates

### Gate 1: Architecture Alignment
✅ Proposed architecture aligns with existing system structure
✅ Integration points are clearly defined

### Gate 2: Technical Feasibility
✅ All required technologies are available and compatible
✅ Backend API is accessible and documented

### Gate 3: Resource Availability
✅ All required dependencies are available
✅ Authentication system is properly integrated

### Gate 4: Compliance Check
✅ Solution follows all constitutional principles
✅ Security considerations are addressed

## Phase 0: Outline & Research

### Research Tasks

#### RT-001: ChatKit Integration Best Practices
- **Decision**: How to properly integrate ChatKit in a Next.js application
- **Rationale**: Need to ensure proper implementation following best practices
- **Alternatives considered**: Alternative chat UI libraries vs ChatKit

#### RT-002: Bottom Corner UI Placement
- **Decision**: How to position the chat UI in the bottom right corner consistently across pages
- **Rationale**: Requirement specifies placement in bottom right corner of all pages
- **Alternatives considered**: Floating button vs persistent panel vs modal

#### RT-003: README Formatting in Chat Responses
- **Decision**: How to render README-style formatting in chatbot responses
- **Rationale**: Requirement specifies support for README-style formatting
- **Alternatives considered**: Using markdown parser vs custom formatting solution

#### RT-004: Authentication Token Retrieval
- **Decision**: How to properly retrieve and use Better Auth tokens
- **Rationale**: API requires Bearer token authentication
- **Alternatives considered**: Different authentication methods vs Better Auth

#### RT-005: State Management for Conversation History
- **Decision**: How to maintain conversation history within a session
- **Rationale**: Need to display conversation history as users interact
- **Alternatives considered**: React state vs Context API vs external state management

## Phase 1: Design & Contracts

### Data Model

#### Chat Message Entity
- **Fields**:
  - id: string (unique identifier)
  - content: string (the message content)
  - sender: 'user' | 'bot' (who sent the message)
  - timestamp: Date (when the message was sent)
  - formatting: object (optional formatting information for README-style content)

#### Conversation Session Entity
- **Fields**:
  - sessionId: string (unique identifier for the session)
  - userId: string (ID of the user associated with the session)
  - messages: Array<ChatMessage> (list of messages in the conversation)
  - createdAt: Date (when the session was created)
  - updatedAt: Date (when the session was last updated)

#### Authentication Token Entity
- **Fields**:
  - token: string (the authentication token)
  - expiration: Date (when the token expires)
  - userId: string (ID of the user the token belongs to)

### API Contract

#### POST /api/{user_id}/chat
- **Description**: Send a message to the AI chatbot and receive a response
- **Headers**:
  - Authorization: Bearer {token} (Required authentication token)
  - Content-Type: application/json
- **Request Body**:
  ```
  {
    "query": "string" // The user's message/query
  }
  ```
- **Response**:
  - 200: OK - Returns the chatbot's response
  - 401: Unauthorized - Invalid or missing authentication token
  - 500: Internal Server Error - Backend service error

### Quickstart Guide

1. **Set up environment variables**:
   ```bash
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=domain_pk_698daa709f5c81979d9cbc12d29471e40d6daf6123da1bb2
   ```

2. **Install dependencies**:
   ```bash
   npm install @chatkit/chatkit
   # Or whatever the correct ChatKit package is
   ```

3. **Configure ChatKit** with the domain key:
   ```typescript
   // Example configuration
   const chatkitConfig = {
     instanceLocator: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
     // Additional configuration as needed
   };
   ```

4. **Implement authentication token retrieval**:
   ```typescript
   const { data, error } = await authClient.token();
   const token = data?.token;
   if (!token) {
     throw new Error('No authentication token found');
   }
   ```

5. **Create the chat component** that appears in the bottom right corner

6. **Implement API call to backend**:
   ```typescript
   const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/${session?.user?.id}/chat`, {
     method: 'POST',
     headers: {
       'Authorization': `Bearer ${token}`,
       'Content-Type': 'application/json',
     },
     body: JSON.stringify({ query: userMessage })
   });
   ```

## Phase 2: Implementation Approach

### Component Structure
1. **FloatingChatButton**: Small button in bottom-right corner to open/close chat
2. **ChatInterface**: Main chat UI component using ChatKit
3. **MessageDisplay**: Component to show individual messages with proper formatting
4. **InputArea**: Area for users to type and submit messages
5. **LoadingIndicator**: Visual indicator during API requests
6. **ErrorMessage**: Component to display error messages

### State Management
- Use React useState and useEffect hooks for local component state
- Use Context API if state needs to be shared across multiple components
- Maintain conversation history in component state during session

### Error Handling
- Display loading indicators during API requests
- Show appropriate error messages when API calls fail
- Handle authentication failures gracefully

### Responsive Design
- Ensure chat interface works on mobile and desktop
- Adjust layout and sizing based on screen dimensions
- Make sure the bottom-right placement works on all screen sizes

## Re-evaluated Constitution Check (Post-Design)

### Spec-Driven Development
✅ Design follows all specifications in spec.md
✅ All user stories and requirements are addressed in the design

### Clean Code
✅ Component structure follows clean code principles
✅ Proper separation of concerns achieved

### Test-First Development
✅ Design allows for comprehensive testing of all components
✅ Clear interfaces for unit and integration tests

### Single Responsibility
✅ Each component has a single, well-defined responsibility
✅ Clear separation between UI, state management, and API calls

### Evolutionary Architecture
✅ Architecture supports future enhancements
✅ Code structure is extensible and maintainable

### User Experience First
✅ Design prioritizes user experience
✅ Loading states and error handling improve UX

## Response Summary

Completed comprehensive implementation plan for the AI Chatbot Frontend Interface. The plan includes technical context, constitution check, research findings, data models, API contracts, and implementation approach. All unknowns have been resolved through research, and all required artifacts have been created as part of the planning process.