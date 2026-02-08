# Production Patterns for MCP Servers

This document outlines advanced patterns for deploying MCP servers in production environments.

## Configuration Management

Use environment variables for configuration management:

```python
import os
from mcp_use.server import MCPServer

server = MCPServer(
    name=os.getenv("MCP_SERVER_NAME", "default-server"),
    version=os.getenv("MCP_SERVER_VERSION", "1.0.0"),
    instructions=os.getenv("MCP_SERVER_DESCRIPTION", "Default MCP server")
)
```

## Health Checks

Implement health check endpoints for monitoring:

```python
from mcp_use.server import MCPServer

server = MCPServer(name="health-check-server")

@server.tool()
def health_check() -> str:
    """Check the health of the server."""
    # Add any internal checks here
    return "OK"
```

## Rate Limiting

Implement rate limiting for expensive operations:

```python
import time
from collections import defaultdict
from mcp_use.server import MCPServer

# Simple rate limiter (consider using redis for distributed systems)
request_counts = defaultdict(list)

def check_rate_limit(client_id: str, max_requests: int = 10, window_seconds: int = 60):
    now = time.time()
    # Remove old requests outside the window
    request_counts[client_id] = [
        req_time for req_time in request_counts[client_id]
        if now - req_time < window_seconds
    ]

    if len(request_counts[client_id]) >= max_requests:
        return False

    request_counts[client_id].append(now)
    return True

@server.tool()
def rate_limited_operation(data: str, client_id: str = "default") -> str:
    """An operation with rate limiting."""
    if not check_rate_limit(client_id):
        return "Rate limit exceeded. Please try again later."

    # Perform the actual operation
    return f"Processed: {data}"
```

## Circuit Breaker Pattern

Implement circuit breakers for resilient operations:

```python
import time
from enum import Enum
from mcp_use.server import MCPServer

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e

    def on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

circuit_breaker = CircuitBreaker()

@server.tool()
def resilient_operation(data: str) -> str:
    """An operation protected by a circuit breaker."""
    def _operation():
        # Simulate potentially failing operation
        if "fail" in data.lower():
            raise Exception("Simulated failure")
        return f"Successfully processed: {data}"

    try:
        return circuit_breaker.call(_operation)
    except Exception as e:
        return f"Circuit breaker prevented operation: {str(e)}"
```

## Graceful Shutdown

Handle shutdown signals gracefully:

```python
import signal
import asyncio
from mcp_use.server import MCPServer

server = MCPServer(name="graceful-shutdown-server")

shutdown_event = asyncio.Event()

def signal_handler(signum, frame):
    print(f"Received signal {signum}, initiating graceful shutdown...")
    shutdown_event.set()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@server.tool()
async def long_running_task(duration: int) -> str:
    """A long-running task that respects shutdown signals."""
    for i in range(duration):
        if shutdown_event.is_set():
            return f"Task interrupted after {i} seconds"

        await asyncio.sleep(1)  # Simulate work

    return f"Task completed after {duration} seconds"
```