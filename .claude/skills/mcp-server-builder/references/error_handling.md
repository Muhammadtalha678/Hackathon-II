# Error Handling and Monitoring for MCP Servers

This document covers comprehensive error handling and monitoring strategies for MCP servers.

## Centralized Error Handling

Implement a centralized error handling system:

```python
from enum import Enum
from typing import Dict, Any
from mcp_use.server import MCPServer, Context
import traceback
import logging

class ErrorCode(Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"

class MCPError(Exception):
    """Custom exception for MCP server errors."""
    def __init__(self, code: ErrorCode, message: str, details: Dict[str, Any] = None):
        self.code = code.value
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

def handle_error(error: Exception, context: str = "") -> Dict[str, Any]:
    """Centralized error handler."""
    if isinstance(error, MCPError):
        error_info = {
            "error_code": error.code,
            "message": error.message,
            "details": error.details
        }
    else:
        # Log the full traceback for unexpected errors
        logging.error(f"Unexpected error in {context}: {str(error)}", exc_info=True)
        error_info = {
            "error_code": ErrorCode.INTERNAL_ERROR.value,
            "message": "An internal error occurred",
            "details": {
                "error_type": type(error).__name__,
                "error_message": str(error)
            }
        }

    return error_info

server = MCPServer(name="error-handling-server")

@server.tool()
def robust_operation(input_data: str, ctx: Context = None) -> str:
    """An operation with robust error handling."""
    try:
        # Validate input
        if not input_data:
            raise MCPError(
                ErrorCode.VALIDATION_ERROR,
                "Input data is required",
                {"field": "input_data", "received_value": input_data}
            )

        # Process the operation
        if "invalid" in input_data.lower():
            raise MCPError(
                ErrorCode.VALIDATION_ERROR,
                "Input contains invalid content",
                {"field": "input_data", "received_value": input_data}
            )

        # Simulate successful processing
        result = f"Processed: {input_data.upper()}"

        # Log success
        if ctx:
            await ctx.log("info", f"Operation completed successfully: {result}")

        return result

    except MCPError as e:
        # Handle known MCP errors
        error_info = handle_error(e, "robust_operation")
        if ctx:
            await ctx.log("error", f"MCP Error: {error_info['message']}")
        return f"Error ({error_info['error_code']}): {error_info['message']}"

    except Exception as e:
        # Handle unexpected errors
        error_info = handle_error(e, "robust_operation")
        if ctx:
            await ctx.log("error", f"Unexpected error: {error_info['message']}")
        return f"Error ({error_info['error_code']}): {error_info['message']}"
```

## Retry Logic

Implement retry logic for transient failures:

```python
import asyncio
import random
from typing import Callable, Type, Tuple

async def retry_with_backoff(
    func: Callable,
    exceptions: Tuple[Type[Exception], ...],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    multiplier: float = 2.0,
    jitter: bool = True
):
    """
    Execute a function with exponential backoff retry logic.
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return await func() if asyncio.iscoroutinefunction(func) else func()
        except exceptions as e:
            last_exception = e

            if attempt == max_retries:
                # Last attempt, raise the exception
                raise last_exception

            # Calculate delay with exponential backoff
            delay = min(base_delay * (multiplier ** attempt), max_delay)

            # Add jitter to prevent thundering herd
            if jitter:
                delay *= (0.5 + random.random() * 0.5)

            await asyncio.sleep(delay)

    # This shouldn't be reached, but included for completeness
    raise last_exception

@server.tool()
async def resilient_external_call(url: str) -> str:
    """Make an external call with retry logic."""
    async def make_request():
        # Simulate an external API call that might fail
        import aiohttp

        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status >= 400:
                    raise MCPError(
                        ErrorCode.INTERNAL_ERROR,
                        f"External API error: {response.status}"
                    )
                return await response.text()

    try:
        result = await retry_with_backoff(
            make_request,
            (MCPError, aiohttp.ClientError, asyncio.TimeoutError),
            max_retries=3,
            base_delay=1.0
        )
        return result
    except Exception as e:
        error_info = handle_error(e, "resilient_external_call")
        return f"Error after retries: {error_info['message']}"
```

## Comprehensive Logging

Implement structured logging for better observability:

```python
import json
import logging
from datetime import datetime
from typing import Dict, Any
from mcp_use.server import MCPServer, Context

# Set up structured logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StructuredLogger:
    @staticmethod
    def log_event(
        event_type: str,
        level: str,
        message: str,
        tool_name: str,
        user_id: str = None,
        request_id: str = None,
        extra_data: Dict[str, Any] = None
    ):
        """Log a structured event."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "level": level,
            "message": message,
            "tool_name": tool_name,
            "user_id": user_id,
            "request_id": request_id,
            "extra_data": extra_data or {}
        }

        logger.log(
            getattr(logging, level.upper()),
            json.dumps(log_data)
        )

structured_logger = StructuredLogger()

@server.tool()
async def instrumented_tool(input_data: str, ctx: Context = None) -> str:
    """A tool with comprehensive instrumentation."""
    import uuid

    request_id = str(uuid.uuid4())
    user_id = "unknown"  # In real implementation, extract from context

    # Log the start of the operation
    structured_logger.log_event(
        event_type="tool_start",
        level="info",
        message="Starting tool execution",
        tool_name="instrumented_tool",
        user_id=user_id,
        request_id=request_id,
        extra_data={"input_length": len(input_data)}
    )

    start_time = datetime.now()

    try:
        # Perform the actual work
        result = input_data.upper()

        duration_ms = (datetime.now() - start_time).total_seconds() * 1000

        # Log successful completion
        structured_logger.log_event(
            event_type="tool_success",
            level="info",
            message="Tool executed successfully",
            tool_name="instrumented_tool",
            user_id=user_id,
            request_id=request_id,
            extra_data={
                "input_length": len(input_data),
                "result_length": len(result),
                "duration_ms": duration_ms
            }
        )

        # Log to MCP client as well
        if ctx:
            await ctx.log("info", f"Tool completed in {duration_ms:.2f}ms")

        return result

    except Exception as e:
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000

        # Log error
        structured_logger.log_event(
            event_type="tool_error",
            level="error",
            message=str(e),
            tool_name="instrumented_tool",
            user_id=user_id,
            request_id=request_id,
            extra_data={
                "input_length": len(input_data),
                "duration_ms": duration_ms,
                "error_type": type(e).__name__
            }
        )

        if ctx:
            await ctx.log("error", f"Tool failed after {duration_ms:.2f}ms: {str(e)}")

        raise
```

## Health Monitoring

Implement health monitoring for your MCP server:

```python
import time
import psutil
import asyncio
from mcp_use.server import MCPServer

class HealthMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        self.last_error_time = None

    def increment_requests(self):
        self.request_count += 1

    def increment_errors(self):
        self.error_count += 1
        self.last_error_time = time.time()

    def get_health_status(self):
        uptime = time.time() - self.start_time
        avg_response_time = 0  # In real implementation, track this
        error_rate = (self.error_count / max(self.request_count, 1)) * 100

        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent

        status = "healthy"
        if error_rate > 10 or cpu_percent > 90 or memory_percent > 90 or disk_percent > 95:
            status = "degraded"
        elif error_rate > 20 or cpu_percent > 95 or memory_percent > 95 or disk_percent > 98:
            status = "unhealthy"

        return {
            "status": status,
            "uptime_seconds": uptime,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate_percent": error_rate,
            "avg_response_time_ms": avg_response_time,
            "last_error_time": self.last_error_time,
            "system_metrics": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "disk_percent": disk_percent
            }
        }

health_monitor = HealthMonitor()

@server.tool()
def get_server_health() -> dict:
    """Return server health information."""
    return health_monitor.get_health_status()

@server.tool()
async def monitored_operation(input_data: str) -> str:
    """An operation that is monitored for health."""
    health_monitor.increment_requests()

    try:
        # Simulate processing
        result = f"Processed: {input_data}"
        return result
    except Exception as e:
        health_monitor.increment_errors()
        raise
```

## Metrics Collection

Collect and expose metrics for monitoring:

```python
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import threading

class MetricsCollector:
    def __init__(self):
        self.lock = threading.Lock()
        self.counters = Counter()
        self.histograms = defaultdict(list)
        self.gauges = {}

    def increment_counter(self, metric_name: str, value: int = 1):
        with self.lock:
            self.counters[metric_name] += value

    def record_histogram(self, metric_name: str, value: float):
        with self.lock:
            self.histograms[metric_name].append(value)

    def set_gauge(self, metric_name: str, value: float):
        with self.lock:
            self.gauges[metric_name] = value

    def get_metrics(self):
        with self.lock:
            metrics = {
                "counters": dict(self.counters),
                "gauges": dict(self.gauges),
            }

            # Calculate histogram summaries
            histograms_summary = {}
            for name, values in self.histograms.items():
                if values:
                    sorted_values = sorted(values)
                    histograms_summary[name] = {
                        "count": len(values),
                        "sum": sum(values),
                        "avg": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "p50": sorted_values[int(len(sorted_values) * 0.5)],
                        "p95": sorted_values[int(len(sorted_values) * 0.95)],
                        "p99": sorted_values[int(len(sorted_values) * 0.99)]
                    }
                else:
                    histograms_summary[name] = {
                        "count": 0,
                        "sum": 0,
                        "avg": 0,
                        "min": 0,
                        "max": 0,
                        "p50": 0,
                        "p95": 0,
                        "p99": 0
                    }

            metrics["histograms"] = histograms_summary
            return metrics

metrics = MetricsCollector()

@server.tool()
def get_server_metrics() -> dict:
    """Return server metrics for monitoring."""
    return metrics.get_metrics()

@server.tool()
async def metric_tracked_operation(input_data: str) -> str:
    """An operation that tracks metrics."""
    start_time = datetime.now()

    try:
        # Track operation
        metrics.increment_counter("operations_total")
        metrics.increment_counter(f"operation_input_size_{len(input_data)}")

        # Simulate processing
        result = f"Processed: {input_data}"

        # Record processing time
        duration = (datetime.now() - start_time).total_seconds() * 1000  # Convert to ms
        metrics.record_histogram("operation_duration_ms", duration)

        return result
    except Exception as e:
        metrics.increment_counter("operation_errors_total")
        raise
```

## Error Recovery Strategies

Implement strategies for error recovery:

```python
from typing import Optional
import asyncio

class FallbackManager:
    def __init__(self):
        self.fallback_enabled = True
        self.circuit_breaker_threshold = 5
        self.circuit_breaker_reset_time = 60  # seconds
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    async def execute_with_fallback(
        self,
        primary_func,
        fallback_func,
        *args,
        **kwargs
    ):
        """Execute primary function with fallback option."""
        if not self.fallback_enabled:
            return await primary_func(*args, **kwargs)

        # Check circuit breaker state
        if self.state == "open":
            time_since_failure = (
                time.time() - self.last_failure_time
                if self.last_failure_time
                else float('inf')
            )
            if time_since_failure > self.circuit_breaker_reset_time:
                # Attempt to close the circuit (half-open state)
                self.state = "half-open"
            else:
                # Circuit is open, use fallback
                return await fallback_func(*args, **kwargs)

        try:
            result = await primary_func(*args, **kwargs)
            # Success, close the circuit if it was half-open
            if self.state == "half-open":
                self.state = "closed"
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            # Open the circuit if threshold is reached
            if self.failure_count >= self.circuit_breaker_threshold:
                self.state = "open"

            # Use fallback
            return await fallback_func(*args, **kwargs)

fallback_manager = FallbackManager()

async def primary_service_call(data: str) -> str:
    """Primary service that might fail."""
    if "fail_primary" in data:
        raise Exception("Primary service failed")
    return f"Primary result: {data}"

async def fallback_service_call(data: str) -> str:
    """Fallback service for when primary fails."""
    return f"Fallback result: {data.replace('fail_primary', 'recovered')}"

@server.tool()
async def resilient_operation_with_fallback(input_data: str) -> str:
    """An operation with fallback strategy."""
    result = await fallback_manager.execute_with_fallback(
        primary_service_call,
        fallback_service_call,
        input_data
    )
    return result
```