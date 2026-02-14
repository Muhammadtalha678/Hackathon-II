# Research Findings: AI Chatbot Frontend Interface

**Feature**: AI Chatbot Frontend Interface  
**Date**: 2026-02-12

## RF-001: ChatKit Integration Best Practices

### Decision
Use ChatKit React components for the chat interface implementation, following the official documentation and best practices for Next.js applications.

### Rationale
The specification explicitly requires using ChatKit library for the chat UI implementation, so we need to follow best practices for integrating it properly with Next.js and TypeScript.

### Alternatives considered
- Alternative chat UI libraries (e.g., react-chat-elements, react-simple-chatbot)
- Building a custom chat UI from scratch

### Research Outcome
ChatKit provides pre-built components for chat interfaces that can be customized. For Next.js integration, we'll need to ensure the component works properly with SSR (Server-Side Rendering) by using dynamic imports with `{ ssr: false }` if needed.

## RF-002: Bottom Corner UI Placement

### Decision
Implement a floating action button in the bottom right corner that expands into a chat interface when clicked.

### Rationale
This approach satisfies the requirement to have the chat interface accessible from the bottom right corner of all pages while not cluttering the main UI space.

### Alternatives considered
- Persistent chat panel taking up space on every page
- Modal that appears from the side
- Full-screen chat overlay

### Research Outcome
A floating button approach is commonly used in many applications (like Intercom, Facebook Messenger) and provides a good balance between accessibility and non-intrusiveness. The button can be fixed positioned using CSS with `position: fixed; bottom: 20px; right: 20px;` and expand into a chat widget when clicked.

## RF-003: README Formatting in Chat Responses

### Decision
Use a markdown parser library like `react-markdown` to render README-style formatting in chatbot responses.

### Rationale
The specification requires support for README-style formatting in chatbot responses, which typically includes headings, lists, code blocks, etc. A dedicated markdown parsing library will handle this properly.

### Alternatives considered
- Custom parsing solution
- Using dangerouslySetInnerHTML (security risk)
- Not supporting formatting

### Research Outcome
Using `react-markdown` with plugins like `remark-gfm` for GitHub Flavored Markdown will properly render README-style formatting including headings, lists, code blocks, and other common markdown elements. This is a secure approach that prevents XSS attacks while still supporting rich formatting.

## RF-004: Authentication Token Retrieval

### Decision
Use the Better Auth client to retrieve the authentication token and include it in API requests as a Bearer token.

### Rationale
The specification requires sending a Bearer token in the header from Better Auth, so we need to properly retrieve this token before making API calls.

### Alternatives considered
- Storing tokens in localStorage (less secure)
- Session cookies
- Other authentication providers

### Research Outcome
Based on the provided example code in the specification, we'll use the Better Auth client to retrieve the token:
```javascript
const { data, error } = await authClient.token();
const { data: session } = await authClient.getSession();
const token = data?.token;
if (!token) {
  throw new Error('No authentication token found');
}
```

## RF-005: State Management for Conversation History

### Decision
Use React's useState hook to maintain conversation history within the chat component during a session.

### Rationale
For a single session's conversation history, local component state is sufficient and follows React best practices. More complex state management would be overkill for this use case.

### Alternatives considered
- Redux or Zustand for global state management
- React Context API
- Storing history in URL parameters
- LocalStorage (for persistence across sessions)

### Research Outcome
Using React's useState to maintain an array of messages is appropriate for managing conversation history within a single session. The state will be initialized as an empty array and updated as new messages are sent and received. When the chat interface is closed and reopened, the history will reset for a new session (unless we implement persistence, which isn't specified).