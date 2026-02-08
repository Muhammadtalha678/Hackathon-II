---
name: mcp-server-builder
description: Build Model Context Protocol (MCP) servers from hello world to professional production systems with comprehensive guidance on architecture, configuration, security, and deployment. Use when building MCP servers for AI assistants, clients, and services using Python or TypeScript implementations.
---

# MCP Server Builder

Build Model Context Protocol (MCP) servers from simple hello world examples to professional production systems with comprehensive guidance on architecture, configuration, security, and deployment.

## Quick Start: Hello World MCP Server

### Python Implementation

Create a basic MCP server using Python:

```python
from mcp_use.server import MCPServer
from mcp_use.server import text

server = MCPServer(
    name="hello-world-server",
    version="1.0.0",
    instructions="A simple hello world MCP server"
)

@server.tool()
def hello(name: str) -> str:
    """Say hello to someone."""
    return text(f"Hello, {name}!")

# Run with stdio for Claude Desktop integration
server.run(transport="stdio")
```

### TypeScript Implementation

Create a basic MCP server using TypeScript:

```typescript
import { MCPServer, text } from "mcp-use/server";
import { z } from "zod";

const server = new MCPServer({ name: "hello-world-server", version: "1.0.0" });

server.tool(
  {
    name: "hello",
    description: "Say hello",
    schema: z.object({ name: z.string().describe("The name to say hello to") }),
  },
  async ({ name }) => {
    return text(`Hello, ${name}!`);
  }
);

export default server;
```

## Development Server Setup

### Python Development Server

Run your MCP server in development mode with debugging and auto-reload:

```python
from mcp_use.server import MCPServer

server = MCPServer(
    name="my-dev-server",
    version="1.0.0",
    instructions="Development MCP server with debugging",
    debug=True,  # Enable development tools
    pretty_print_jsonrpc=True,  # Beautiful JSON-RPC logs
)

@server.tool()
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    # Be cautious with eval() in production!
    return eval(expression)

# Run with multiple transport options for development
server.run(
    transport="streamable-http",  # HTTP transport for web clients and testing
    host="127.0.0.1",
    port=8000,
    reload=True,  # Auto-reload on code changes
    debug=True    # Enable debug features
)
```

### TypeScript Development Server

```typescript
import server from "./server";

// Development: Run with HTTP transport for easy testing
server.listen({ port: 8000 });
console.log("MCP Server running at http://localhost:8000");
console.log("Inspector available at http://localhost:8000/inspector");
```

## Advanced Features

### Context-Aware Tools (Python)

Leverage advanced context features for enhanced MCP server functionality:

```python
from mcp_use.server import MCPServer, Context
from dataclasses import dataclass

server = MCPServer(name="advanced-server")

@server.tool()
async def smart_search(query: str, ctx: Context) -> str:
    """Intelligent search with LLM refinement."""
    # Use sampling to request LLM assistance from the client
    result = await ctx.sample(
        messages=f"Refine this search query: {query}",
        max_tokens=100,
        temperature=0.7,
        model_preferences={"hints": [{"name": "claude-3-5-sonnet"}]}
    )
    refined_query = result.content.text

    # Use elicitation to get structured input from user
    @dataclass
    class SearchFilters:
        date_range: str
        categories: list[str]
        max_results: int = 10

    filters = await ctx.elicit(
        message="Please specify search filters",
        schema=SearchFilters  # Supports both Pydantic and dataclasses
    )

    # Perform search with refined query and filters...
    return f"Results for '{refined_query}' with filters: {filters.data}"

@server.tool()
async def dynamic_tool_registration(name: str, ctx: Context) -> str:
    """Dynamically register a new tool."""
    # Notify clients about tool list changes
    await ctx.send_tool_list_changed()
    return f"Added tool: {name}"
```

### Context Logging (TypeScript)

Log messages directly to clients from within tools:

```typescript
server.tool({
  name: 'process_data',
  description: 'Process data with progress logging',
  schema: z.object({
    items: z.array(z.string())
  })
}, async ({ items }, ctx) => {
  // Log the start of processing
  await ctx.log('info', 'Starting data processing');

  // Debug-level logging for detailed information
  await ctx.log('debug', `Processing ${items.length} items`, 'my-tool');

  for (const item of items) {
    // Log warnings when needed
    if (!item.trim()) {
      await ctx.log('warning', 'Empty item found, skipping');
      continue;
    }

    try {
      await processItem(item);
    } catch (err) {
      // Log errors without throwing
      await ctx.log('error', `Failed to process item: ${err.message}`);
    }
  }

  await ctx.log('info', 'Processing completed');
  return text('All items processed');
})
```

## Production Deployment

### Python Production Server

Configure your MCP server for production deployment:

```python
from mcp_use.server import MCPServer

server = MCPServer(
    name="production-server",
    version="1.0.0",
    instructions="Production-ready MCP server",
    debug=False,  # Disable debugging in production
    pretty_print_jsonrpc=False  # Reduce logging overhead
)

@server.tool()
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression safely."""
    # Implement safe evaluation in production
    import ast
    import operator

    # Safe evaluation using AST (avoid eval()!)
    allowed_operators = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.Mod: operator.mod,
        ast.USub: operator.neg
    }

    def eval_expr(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            left = eval_expr(node.left)
            right = eval_expr(node.right)
            return allowed_operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            operand = eval_expr(node.operand)
            return allowed_operators[type(node.op)](operand)
        else:
            raise TypeError(node)

    try:
        node = ast.parse(expression, mode='eval')
        return float(eval_expr(node.body))
    except Exception:
        raise ValueError(f"Invalid expression: {expression}")

# Production server configuration
server.run(
    transport="streamable-http",
    host="0.0.0.0",  # Bind to all interfaces
    port=8000,
    reload=False,    # Disable auto-reload
    debug=False      # Disable debug features
)
```

### Docker Configuration for Production

Create a secure Dockerfile for your MCP server:

```dockerfile
FROM node:18-alpine

# Create non-root user
RUN addgroup -S mcpuser && adduser -S mcpuser -G mcpuser

# Install security updates
RUN apk update && apk upgrade && \
    apk add --no-cache ca-certificates && \
    rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Set ownership and permissions
RUN chown -R mcpuser:mcpuser /app
USER mcpuser

# Expose port
EXPOSE 8000

# Run application
CMD ["node", "main.js"]
```

### Kubernetes Deployment

Deploy your MCP server to Kubernetes with proper configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: your-registry/mcp-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DEBUG
          value: "0"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

---
apiVersion: v1
kind: Service
metadata:
  name: mcp-server
spec:
  selector:
    app: mcp-server
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

## Transport Configuration

Choose the appropriate transport for your MCP server:

### Stdio Transport
For MCP clients like Claude Desktop that connect directly via stdin/stdout:

```python
server.run(transport="stdio")
```

### HTTP Transport (Recommended for Production)
For web clients, testing, and external access:

```python
server.run(
    transport="streamable-http",
    host="0.0.0.0",
    port=8000
)
```

## Error Handling and Logging

### Python Error Handling

Implement comprehensive error handling in your tools:

```python
import logging

logger = logging.getLogger(__name__)

@server.tool()
def robust_tool(data: str) -> str:
    """A tool with comprehensive error handling."""
    logger.info(f"Processing data: {data}")

    try:
        # Your tool logic here
        result = process_data_safely(data)
        logger.debug(f"Processing result: {result}")
        return text(result)
    except ValueError as e:
        logger.error(f"Value error in tool: {e}")
        return text(f"Error: Invalid input - {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in tool: {e}", exc_info=True)
        return text("Error: An unexpected error occurred")
```

### Debug Levels

Control the verbosity of your server logs:

```bash
# Production: Clean logs only
DEBUG=0 python server.py

# Debug: Clean logs + dev routes (/docs, /inspector, /openmcp.json)
DEBUG=1 python server.py

# Verbose: Everything + JSON-RPC logging with pretty printing
DEBUG=2 python server.py
```

## Security Considerations

When building MCP servers, always follow security best practices:

1. Validate all inputs to prevent injection attacks
2. Use safe evaluation methods instead of eval() in production
3. Implement proper authentication if needed
4. Restrict access to development tools in production
5. Sanitize and validate all data passed between client and server
6. Consider rate limiting for high-volume operations
7. Keep dependencies up to date with security patches

## Next Steps

For more advanced MCP server patterns and best practices, refer to the following resources:
- [PRODUCTION_PATTERNS.md](references/production_patterns.md) - Advanced production patterns
- [SECURITY_BEST_PRACTICES.md](references/security_best_practices.md) - Security guidelines
- [ERROR_HANDLING.md](references/error_handling.md) - Comprehensive error handling strategies
- [MONITORING.md](references/monitoring.md) - Server monitoring and observability