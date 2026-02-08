# Security Best Practices for MCP Servers

This document outlines security considerations and best practices when building and deploying MCP servers.

## Input Validation

Always validate and sanitize inputs to prevent injection attacks:

```python
import re
from typing import Optional
from mcp_use.server import MCPServer, text

server = MCPServer(name="secure-input-server")

def validate_filename(filename: str) -> bool:
    """Validate filename to prevent directory traversal."""
    # Prevent path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        return False

    # Allow only alphanumeric, dots, hyphens, and underscores
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        return False

    # Prevent common dangerous extensions
    dangerous_exts = ['.exe', '.bat', '.cmd', '.sh', '.php', '.jsp']
    if any(filename.lower().endswith(ext) for ext in dangerous_exts):
        return False

    return True

@server.tool()
def safe_file_access(filename: str) -> str:
    """Safely access a file with validation."""
    if not validate_filename(filename):
        return text("Invalid filename")

    # Proceed with file access if validated
    try:
        with open(f"./safe_directory/{filename}", 'r') as f:
            return text(f.read())
    except FileNotFoundError:
        return text("File not found")
    except Exception as e:
        return text(f"Error reading file: {str(e)}")
```

## Authentication and Authorization

Implement authentication where needed:

```python
import jwt
import os
from datetime import datetime, timedelta
from mcp_use.server import MCPServer, Context

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

def create_token(user_id: str) -> str:
    """Create a JWT token for a user."""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(token: str) -> Optional[str]:
    """Verify a JWT token and return user_id if valid."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@server.tool()
def authenticated_operation(auth_token: str, data: str) -> str:
    """An operation that requires authentication."""
    user_id = verify_token(auth_token)
    if not user_id:
        return "Authentication required"

    # Process the operation for the authenticated user
    return f"Processed for user {user_id}: {data}"
```

## Sanitization Functions

Implement sanitization for various data types:

```python
import html
import re
from urllib.parse import urlparse
import bleach

def sanitize_html(content: str) -> str:
    """Sanitize HTML content."""
    # Use bleach to sanitize HTML
    allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li']
    allowed_attributes = {}
    return bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes)

def sanitize_sql_identifier(identifier: str) -> str:
    """Sanitize SQL identifiers."""
    # Only allow alphanumeric characters and underscores
    return re.sub(r'[^a-zA-Z0-9_]', '_', identifier)

def validate_url(url: str) -> bool:
    """Validate URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

@server.tool()
def safe_html_operation(content: str) -> str:
    """Process HTML content safely."""
    sanitized_content = sanitize_html(content)
    return f"Processed content: {sanitized_content}"
```

## Secure Configuration

Use environment variables and secure defaults:

```python
import os
from mcp_use.server import MCPServer

# Load configuration securely
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
SSL_REQUIRED = os.getenv("SSL_REQUIRED", "true").lower() == "true"

# Never log sensitive information
def log_safe_config():
    """Log configuration without sensitive data."""
    print(f"Database host: {DB_HOST}:{DB_PORT}")
    print(f"SSL Required: {SSL_REQUIRED}")
    # Don't log DB_USER or DB_PASSWORD

server = MCPServer(
    name="secure-config-server",
    version="1.0.0"
)
```

## Resource Limits

Implement resource limits to prevent abuse:

```python
import psutil
import os
from mcp_use.server import MCPServer

def check_system_resources():
    """Check system resources and return True if within limits."""
    # Check memory usage
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > 80:
        return False, f"Memory usage too high: {memory_percent}%"

    # Check disk space
    disk_usage = psutil.disk_usage('/').percent
    if disk_usage > 90:
        return False, f"Disk usage too high: {disk_usage}%"

    # Check CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 90:
        return False, f"CPU usage too high: {cpu_percent}%"

    return True, "Resources within limits"

@server.tool()
def resource_conscious_operation(data: str) -> str:
    """An operation that checks system resources before proceeding."""
    resources_ok, message = check_system_resources()
    if not resources_ok:
        return f"Insufficient resources: {message}"

    # Proceed with the operation
    return f"Processed safely: {data[:100]}..."
```

## Secure Transport

Ensure secure transport for sensitive data:

```python
import ssl
import os
from mcp_use.server import MCPServer

def get_ssl_context():
    """Get SSL context for secure connections."""
    if os.getenv("ENABLE_SSL", "false").lower() == "true":
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        cert_file = os.getenv("CERT_FILE")
        key_file = os.getenv("KEY_FILE")

        if cert_file and key_file:
            context.load_cert_chain(cert_file, key_file)
        else:
            # Create self-signed certificate for testing
            context.load_default_certs()

        return context
    return None

# The server will automatically use SSL if context is provided
# when running with HTTP transport
```

## Additional Security Measures

Consider these additional security measures:

1. **Rate Limiting**: Prevent abuse by limiting requests per user/IP
2. **Input Size Limits**: Limit the size of incoming data
3. **Time-based Validations**: Expire tokens and sessions appropriately
4. **Secure Dependencies**: Keep all dependencies updated and scan for vulnerabilities
5. **Network Isolation**: Deploy in isolated networks when possible
6. **Monitoring and Logging**: Log security events without exposing sensitive data
7. **Principle of Least Privilege**: Give the server minimal required permissions
8. **Data Encryption**: Encrypt sensitive data in transit and at rest