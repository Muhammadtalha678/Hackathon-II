# Quickstart Guide: AI Chatbot Frontend Interface

**Feature**: AI Chatbot Frontend Interface  
**Date**: 2026-02-12

## Prerequisites

Before starting the implementation, ensure you have:

- Node.js (v16 or later)
- npm or yarn package manager
- Better Auth configured in your Next.js application
- Access to the backend API at https://muhammad51059579-phase-3-backend.hf.space

## Setup Environment

1. **Set up environment variables** in your `.env.local` file:
   ```bash
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=domain_pk_698daa709f5c81979d9cbc12d29471e40d6daf6123da1bb2
   NEXT_PUBLIC_BACKEND_URL=https://muhammad51059579-phase-3-backend.hf.space
   ```

2. **Install required dependencies**:
   ```bash
   npm install @chatkit/provider react-markdown remark-gfm
   # Or if using yarn
   yarn add @chatkit/provider react-markdown remark-gfm
   ```

## Implementation Steps

### Step 1: Create the Floating Chat Button

Create a component that appears as a floating button in the bottom right corner of all pages:

```tsx
// components/FloatingChatButton.tsx
import { useState } from 'react';
import ChatInterface from './ChatInterface';

const FloatingChatButton = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed bottom-5 right-5 z-50">
      {isOpen ? (
        <ChatInterface onClose={() => setIsOpen(false)} />
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-600 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg hover:bg-blue-700 transition-colors"
          aria-label="Open chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      )}
    </div>
  );
};

export default FloatingChatButton;
```

### Step 2: Integrate the Chat Button into Your Layout

Add the floating chat button to your main layout component so it appears on all pages:

```tsx
// layouts/MainLayout.tsx (or wherever your main layout is)
import FloatingChatButton from '../components/FloatingChatButton';

const MainLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="relative min-h-screen">
      {/* Your existing layout content */}
      <main>{children}</main>
      
      {/* Floating chat button appears on all pages */}
      <FloatingChatButton />
    </div>
  );
};

export default MainLayout;
```

### Step 3: Create the Chat Interface Component

Create the main chat interface component using ChatKit:

```tsx
// components/ChatInterface.tsx
import { useState, useRef, useEffect } from 'react';
import { useAuth } from 'better-auth/react'; // Adjust import based on your auth setup
import MessageDisplay from './MessageDisplay';
import LoadingIndicator from './LoadingIndicator';
import ErrorMessage from './ErrorMessage';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

interface ChatInterfaceProps {
  onClose: () => void;
}

const ChatInterface = ({ onClose }: ChatInterfaceProps) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { authClient } = useAuth(); // Adjust based on your auth setup
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputValue.trim()) return;

    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Get authentication token
      const { data: tokenData, error: tokenError } = await authClient.token();
      const { data: sessionData } = await authClient.getSession();
      
      const token = tokenData?.token;
      if (!token) {
        throw new Error('No authentication token found');
      }

      const userId = sessionData?.user?.id;
      if (!userId) {
        throw new Error('User not authenticated');
      }

      // Call the backend API
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: inputValue })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to get response from chatbot');
      }

      const responseData = await response.json();
      
      // Add bot response to the chat
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: responseData.response,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-80 h-96 bg-white border border-gray-300 rounded-lg shadow-xl flex flex-col overflow-hidden">
      {/* Chat header */}
      <div className="bg-blue-600 text-white p-3 flex justify-between items-center">
        <h3 className="font-semibold">AI Assistant</h3>
        <button 
          onClick={onClose}
          className="text-white hover:text-gray-200 focus:outline-none"
          aria-label="Close chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      {/* Chat messages container */}
      <div className="flex-1 overflow-y-auto p-3 bg-gray-50">
        {messages.map((message) => (
          <MessageDisplay key={message.id} message={message} />
        ))}
        {isLoading && <LoadingIndicator />}
        {error && <ErrorMessage message={error} />}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <form onSubmit={handleSubmit} className="border-t border-gray-300 p-2 bg-white">
        <div className="flex">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 border border-gray-300 rounded-l px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            className={`bg-blue-600 text-white px-4 py-2 rounded-r ${
              isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'
            }`}
            disabled={isLoading || !inputValue.trim()}
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
```

### Step 4: Create Supporting Components

Create the MessageDisplay component to show individual messages:

```tsx
// components/MessageDisplay.tsx
import { Message } from './ChatInterface';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MessageDisplayProps {
  message: Message;
}

const MessageDisplay = ({ message }: MessageDisplayProps) => {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`mb-3 ${isUser ? 'text-right' : 'text-left'}`}>
      <div
        className={`inline-block max-w-xs md:max-w-md px-3 py-2 rounded-lg ${
          isUser 
            ? 'bg-blue-500 text-white rounded-br-none' 
            : 'bg-gray-200 text-gray-800 rounded-bl-none'
        }`}
      >
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {message.content}
        </ReactMarkdown>
      </div>
      <div className="text-xs text-gray-500 mt-1 px-2">
        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
    </div>
  );
};

export default MessageDisplay;
```

Create the LoadingIndicator component:

```tsx
// components/LoadingIndicator.tsx
const LoadingIndicator = () => {
  return (
    <div className="mb-3 text-left">
      <div className="inline-block bg-gray-200 text-gray-800 px-3 py-2 rounded-lg rounded-bl-none">
        <div className="flex space-x-1">
          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingIndicator;
```

Create the ErrorMessage component:

```tsx
// components/ErrorMessage.tsx
interface ErrorMessageProps {
  message: string;
}

const ErrorMessage = ({ message }: ErrorMessageProps) => {
  return (
    <div className="mb-3 text-left">
      <div className="inline-block bg-red-100 text-red-800 px-3 py-2 rounded-lg rounded-bl-none border border-red-300">
        {message}
      </div>
    </div>
  );
};

export default ErrorMessage;
```

### Step 5: Add CSS Styling

Add the following CSS to your global styles (e.g., in `styles/globals.css`):

```css
/* Smooth scrolling for chat messages */
.chat-container {
  scroll-behavior: smooth;
}

/* Animation for loading dots */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.animate-bounce {
  animation: bounce 1s infinite;
}

.delay-75 {
  animation-delay: 0.25s;
}

.delay-150 {
  animation-delay: 0.5s;
}
```

## Testing the Implementation

1. **Unit Tests**: Create unit tests for each component focusing on:
   - Message rendering
   - Form submission handling
   - Error handling
   - Loading state display

2. **Integration Tests**: Test the complete flow:
   - Opening/closing the chat interface
   - Sending messages and receiving responses
   - Authentication token retrieval
   - API call handling

3. **Manual Testing**: Verify:
   - The chat button appears in the bottom right corner on all pages
   - The chat interface opens and closes properly
   - Messages are displayed with proper styling
   - README-style formatting renders correctly
   - Loading indicators appear during API calls
   - Error messages display appropriately

## Deployment

1. Ensure environment variables are properly set in your deployment environment
2. Verify the backend API endpoint is accessible from your deployed frontend
3. Test the chat functionality in your production environment