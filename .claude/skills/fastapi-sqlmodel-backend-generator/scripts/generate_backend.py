#!/usr/bin/env python3
"""
FastAPI SQLModel Backend Generator Script

This script generates a clean, production-ready FastAPI backend project structure
with SQLModel ORM, supporting any SQL database and ready for any domain/business logic.
"""
import os
import argparse
from pathlib import Path

def create_directory(path):
    """Create a directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)

def write_file(path, content):
    """Write content to a file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_backend(project_name="backend", database_type="postgresql", include_examples=True, python_version="3.11"):
    """Generate the FastAPI backend project structure."""

    # Create project directory
    create_directory(project_name)

    # Create src directory structure
    create_directory(f"{project_name}/src/models")
    create_directory(f"{project_name}/src/controllers")
    create_directory(f"{project_name}/src/routers")
    create_directory(f"{project_name}/src/lib")
    create_directory(f"{project_name}/tests")

    # Generate src/lib/db_connect.py
    db_connect_content = '''"""
Database connection manager using SQLModel.
Handles connection lifecycle, session management, and table creation.
Works with any SQL database supported by SQLAlchemy.
"""
from sqlmodel import SQLModel, Session, create_engine
from typing import Generator, Optional
from sqlalchemy.engine import Engine

class DBConfig:
    """
    Generic database configuration and connection manager.

    Supports any SQL database (PostgreSQL, MySQL, SQL Server, SQLite, etc.)
    through SQLAlchemy connection URLs.

    Attributes:
        url: Database connection URL
        engine: SQLAlchemy engine instance
    """

    def __init__(self, url: str, echo: bool = False, pool_pre_ping: bool = True):
        """
        Initialize database configuration.

        Args:
            url: Database connection URL (SQLAlchemy format)
            echo: Whether to log SQL statements (default: False)
            pool_pre_ping: Test connections before using (default: True)
        """
        self.url = url
        self.echo = echo
        self.pool_pre_ping = pool_pre_ping
        self.engine: Optional[Engine] = None

    def open_connection(self) -> None:
        """
        Open database connection and create engine.

        Raises:
            Exception: If connection fails
        """
        self.engine = create_engine(
            url=self.url,
            pool_pre_ping=self.pool_pre_ping,
            echo=self.echo
        )
        try:
            with self.engine.connect() as conn:
                print("✓ Database connected successfully")
                print(f"  Database URL: {self._mask_password(self.url)}")
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
            raise Exception(f"Error connecting to database: {e}")

    def close_connection(self) -> None:
        """Close database connection and dispose engine."""
        if self.engine:
            self.engine.dispose()
            print("✓ Database disconnected successfully")

    def create_tables(self) -> None:
        """
        Create all tables defined in SQLModel metadata.

        Note: Imports all model files to ensure they're registered
        with SQLModel.metadata before table creation.
        """
        if not self.engine:
            raise Exception("Database engine not initialized. Call open_connection() first.")

        # Import all models here to register them with metadata
        # Example: from src.models import user_model, product_model

        SQLModel.metadata.create_all(self.engine)
        print("✓ Database tables created successfully")

    def get_session(self) -> Generator[Session, None, None]:
        """
        Get database session generator for dependency injection.

        Yields:
            Session: SQLModel database session

        Example:
            SessionDep = Annotated[Session, Depends(db.get_session)]
        """
        if not self.engine:
            raise Exception("Database engine not initialized. Call open_connection() first.")

        with Session(self.engine) as session:
            yield session

    @staticmethod
    def _mask_password(url: str) -> str:
        """Mask password in URL for logging."""
        if "://" in url and "@" in url:
            protocol, rest = url.split("://", 1)
            if "@" in rest:
                credentials, host = rest.split("@", 1)
                if ":" in credentials:
                    username, _ = credentials.split(":", 1)
                    return f"{protocol}://{username}:****@{host}"
        return url
'''
    write_file(f"{project_name}/src/lib/db_connect.py", db_connect_content)

    # Generate src/lib/env_config.py
    env_config_content = '''"""
Environment configuration loader.
Loads database credentials and application settings from .env file.
"""
from dotenv import load_dotenv
from sqlalchemy import URL
import os
from typing import Optional

# Load environment variables
load_dotenv()

class Config:
    """
    Application configuration loaded from environment variables.

    Supports multiple database types through flexible configuration.
    """

    # Application Settings
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Backend")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database Settings
    DB_DRIVER: str = os.getenv("DB_DRIVER", "postgresql+psycopg2")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: Optional[str] = os.getenv("DB_PORT")  # Optional
    DB_NAME: str = os.getenv("DB_NAME", "database")

    # Authentication Settings
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-jwt-key-change-this-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Optional: For databases requiring additional query parameters
    DB_DRIVER_ODBC: Optional[str] = os.getenv("DB_DRIVER_ODBC")  # For SQL Server

    @classmethod
    def get_database_url(cls) -> str:
        """
        Construct database URL from environment variables.

        Returns:
            str: Database connection URL

        Supports:
            - PostgreSQL: postgresql+psycopg2://user:pass@host:5432/db
            - MySQL: mysql+pymysql://user:pass@host:3306/db
            - SQL Server: mssql+pyodbc://user:pass@host:1433/db?driver=...
            - SQLite: sqlite:///./database.db
            - Neon: postgresql+psycopg2://user:pass@neon-host/db
        """
        # Special case for SQLite
        if cls.DB_DRIVER.startswith("sqlite"):
            return f"sqlite:///./{cls.DB_NAME}.db"

        # Build query parameters
        query = {}
        if cls.DB_DRIVER_ODBC:
            query["driver"] = cls.DB_DRIVER_ODBC

        # Construct URL
        url_obj = URL.create(
            drivername=cls.DB_DRIVER,
            username=cls.DB_USERNAME,
            password=cls.DB_PASSWORD,
            host=cls.DB_HOST,
            port=int(cls.DB_PORT) if cls.DB_PORT else None,
            database=cls.DB_NAME,
            query=query if query else None
        )

        return str(url_obj)
'''
    write_file(f"{project_name}/src/lib/env_config.py", env_config_content)

    # Generate src/lib/session.py
    session_content = '''"""
Session dependency for FastAPI route handlers.
Provides reusable database session through dependency injection.
"""
from fastapi import Request, Depends
from typing import Annotated
from sqlmodel import Session

def get_session_from_request(request: Request):
    """
    Get database session from application state.

    Args:
        request: FastAPI request object containing app state

    Yields:
        Session: Database session instance

    Example Usage in Router:
        @router.get("/items")
        def get_items(session: SessionDep):
            items = session.exec(select(Item)).all()
            return items
    """
    db = request.app.state.db_init
    yield from db.get_session()

# Type annotation for session dependency injection
# Use this in all route handlers that need database access
SessionDep = Annotated[Session, Depends(get_session_from_request)]
'''
    write_file(f"{project_name}/src/lib/session.py", session_content)

    # Generate src/lib/exceptions.py
    exceptions_content = '''"""
Custom exception classes for the application.
Provides structured error handling across the application.
"""
from fastapi import HTTPException, status

class DatabaseException(HTTPException):
    """Base exception for database-related errors."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {detail}"
        )

class NotFoundException(HTTPException):
    """Exception for resource not found errors."""

    def __init__(self, resource: str, identifier: str | int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id '{identifier}' not found"
        )

class ValidationException(HTTPException):
    """Exception for validation errors."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {detail}"
        )

class ConflictException(HTTPException):
    """Exception for resource conflict errors (e.g., duplicate entries)."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Conflict: {detail}"
        )
'''

    # Generate src/lib/exceptions.py
    write_file(f"{project_name}/src/lib/exceptions.py", exceptions_content)

    # Generate src/lib/auth.py
    auth_content = '''"""
Authentication middleware and utilities using JWT tokens.
Verifies access tokens from either headers or cookies.
"""
from fastapi import HTTPException, Request, status, Depends
import jwt
from typing import Optional
from sqlmodel import Session, select

from src.models.user_model import User  # You'll need to create this model
from src.lib.env_config import Config
from src.lib.session import get_session_from_request
from src.lib.exceptions import ValidationException


def verify_token_middleware(
    request: Request,
    session: Session = Depends(get_session_from_request)
):
    """
    Verify JWT token from either header or cookie.

    Args:
        request: FastAPI request object
        session: Database session (injected)

    Returns:
        User: Authenticated user object

    Raises:
        HTTPException: If token is missing, invalid, expired, or user not found
    """
    # Try to get token from header first, then from cookies
    auth_header = request.headers.get("authorization")
    cookie_token = request.cookies.get("access_token")

    token: Optional[str] = None

    # Check header for Bearer token
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Remove "Bearer " prefix
    elif cookie_token:
        token = cookie_token  # Use cookie token if no header token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token missing from header or cookies"
        )

    # Decode and verify the token
    try:
        decoded_data = jwt.decode(
            token,
            Config.BETTER_AUTH_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        email = decoded_data["email"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

    # Verify user exists in database
    try:
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying user: {str(e)}"
        )


def get_current_user(
    request: Request,
    session: Session = Depends(get_session_from_request)
):
    """
    Get current authenticated user from token.

    This is a convenience function that can be used as a dependency.

    Args:
        request: FastAPI request object
        session: Database session (injected)

    Returns:
        User: Authenticated user object
    """
    return verify_token_middleware(request, session)
'''
    write_file(f"{project_name}/src/lib/auth.py", auth_content)

    # Generate src/models/base.py
    base_model_content = '''"""
Base model with common fields and utilities.
All application models should inherit from these base classes.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class TimestampMixin(SQLModel):
    """
    Mixin for adding timestamp fields to models.

    Provides created_at and updated_at fields for tracking
    record creation and modification times.
    """
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when record was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when record was last updated"
    )

class BaseModel(SQLModel):
    """
    Base model for all database models.

    Provides common fields and methods that all models should have.
    Inherit from this class when creating new models.
    """
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Primary key"
    )

    class Config:
        """SQLModel configuration."""
        # Add any model-wide configuration here
        pass
'''
    write_file(f"{project_name}/src/models/base.py", base_model_content)

    # Generate example model if requested
    if include_examples:
        example_model_content = '''"""
Example model demonstrating best practices.
Replace this with your actual domain models.

Examples of models you might create:
- User, Product, Order, Payment (E-commerce)
- Post, Comment, Like (Blog/Social Media)
- Inventory, Supplier, Purchase (Inventory Management)
- Patient, Doctor, Appointment (Healthcare)
"""
from sqlmodel import Field
from typing import Optional
from src.models.base import BaseModel, TimestampMixin

class ItemBase(SQLModel):
    """
    Base schema for Item with common fields.
    Used for validation in create/update operations.
    """
    name: str = Field(
        min_length=1,
        max_length=200,
        index=True,
        description="Item name"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Item description"
    )
    price: float = Field(
        gt=0,
        description="Item price (must be positive)"
    )
    quantity: int = Field(
        default=0,
        ge=0,
        description="Available quantity"
    )

class ItemCreate(ItemBase):
    """
    Schema for creating new items.
    Inherits all fields from ItemBase.
    """
    pass

class ItemUpdate(SQLModel):
    """
    Schema for updating existing items.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: Optional[float] = Field(default=None, gt=0)
    quantity: Optional[int] = Field(default=None, ge=0)

class Item(ItemBase, BaseModel, TimestampMixin, table=True):
    """
    Item database model.

    This is an example model - replace with your actual domain models.

    Inherits from:
        - ItemBase: Business logic fields
        - BaseModel: Common fields (id, etc.)
        - TimestampMixin: Timestamp fields (created_at, updated_at)

    Attributes:
        id: Primary key (from BaseModel)
        name: Item name
        description: Item description
        price: Item price
        quantity: Available quantity
        created_at: Creation timestamp (from TimestampMixin)
        updated_at: Last update timestamp (from TimestampMixin)
    """
    __tablename__ = "items"  # Explicit table name
'''
        write_file(f"{project_name}/src/models/example_model.py", example_model_content)

    # Generate example controller if requested
    if include_examples:
        example_controller_content = '''"""
Example controller demonstrating CRUD operations.
Replace this with your actual business logic controllers.

Controllers contain business logic and database operations.
They should be called from routers/endpoints.
"""
from sqlmodel import select
from src.models.example_model import Item, ItemCreate, ItemUpdate
from src.lib.session import SessionDep
from src.lib.exceptions import NotFoundException, DatabaseException
from typing import List, Optional

def get_all_items(session: SessionDep, skip: int = 0, limit: int = 100) -> List[Item]:
    """
    Retrieve all items with pagination.

    Args:
        session: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        List[Item]: List of items

    Raises:
        DatabaseException: If query fails
    """
    try:
        statement = select(Item).offset(skip).limit(limit)
        items = session.exec(statement).all()
        return list(items)
    except Exception as e:
        raise DatabaseException(f"Failed to retrieve items: {str(e)}")

def get_item_by_id(session: SessionDep, item_id: int) -> Item:
    """
    Retrieve specific item by ID.

    Args:
        session: Database session
        item_id: Item identifier

    Returns:
        Item: Item object

    Raises:
        NotFoundException: If item not found
        DatabaseException: If query fails
    """
    try:
        item = session.get(Item, item_id)
        if not item:
            raise NotFoundException("Item", item_id)
        return item
    except NotFoundException:
        raise
    except Exception as e:
        raise DatabaseException(f"Failed to retrieve item: {str(e)}")

def search_items(session: SessionDep, query: str) -> List[Item]:
    """
    Search items by name.

    Args:
        session: Database session
        query: Search query string

    Returns:
        List[Item]: List of matching items

    Raises:
        DatabaseException: If query fails
    """
    try:
        statement = select(Item).where(Item.name.contains(query))
        items = session.exec(statement).all()
        return list(items)
    except Exception as e:
        raise DatabaseException(f"Failed to search items: {str(e)}")

def create_item(session: SessionDep, item_data: ItemCreate) -> Item:
    """
    Create new item in database.

    Args:
        session: Database session
        item_data: Item creation data

    Returns:
        Item: Created item object

    Raises:
        DatabaseException: If creation fails
    """
    try:
        item = Item.model_validate(item_data)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Failed to create item: {str(e)}")

def update_item(session: SessionDep, item_id: int, item_data: ItemUpdate) -> Item:
    """
    Update existing item.

    Args:
        session: Database session
        item_id: Item identifier
        item_data: Updated item data (partial updates supported)

    Returns:
        Item: Updated item object

    Raises:
        NotFoundException: If item not found
        DatabaseException: If update fails
    """
    try:
        item = session.get(Item, item_id)
        if not item:
            raise NotFoundException("Item", item_id)

        # Update only provided fields
        update_data = item_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

        # Update the updated_at timestamp
        from datetime import datetime
        item.updated_at = datetime.utcnow()

        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except NotFoundException:
        raise
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Failed to update item: {str(e)}")

def delete_item(session: SessionDep, item_id: int) -> dict:
    """
    Delete item from database.

    Args:
        session: Database session
        item_id: Item identifier

    Returns:
        dict: Success message with deleted item details

    Raises:
        NotFoundException: If item not found
        DatabaseException: If deletion fails
    """
    try:
        item = session.get(Item, item_id)
        if not item:
            raise NotFoundException("Item", item_id)

        session.delete(item)
        session.commit()
        return {
            "success": True,
            "message": f"Item '{item.name}' deleted successfully",
            "deleted_id": item_id
        }
    except NotFoundException:
        raise
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Failed to delete item: {str(e)}")
'''
        write_file(f"{project_name}/src/controllers/example_controller.py", example_controller_content)

    # Generate example router if requested
    if include_examples:
        example_router_content = '''"""
Example router demonstrating RESTful API endpoints.
Replace this with your actual domain routers.

Routers define HTTP endpoints and delegate business logic to controllers.
"""
from fastapi import APIRouter, Query
from src.lib.session import SessionDep
from src.models.example_model import Item, ItemCreate, ItemUpdate
from src.controllers import example_controller
from typing import List

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/items",
    tags=["Items (Example)"]
)

@router.get("/", response_model=List[Item])
def list_items(
    session: SessionDep,
    skip: int = Query(default=0, ge=0, description="Number of items to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of items to return")
) -> List[Item]:
    """
    List all items with pagination.

    Args:
        session: Database session (injected)
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List[Item]: List of items
    """
    return example_controller.get_all_items(session, skip=skip, limit=limit)

@router.get("/search", response_model=List[Item])
def search_items(
    session: SessionDep,
    q: str = Query(..., min_length=1, description="Search query")
) -> List[Item]:
    """
    Search items by name.

    Args:
        session: Database session (injected)
        q: Search query string

    Returns:
        List[Item]: List of matching items
    """
    return example_controller.search_items(session, query=q)

@router.get("/{item_id}", response_model=Item)
def get_item(
    item_id: int,
    session: SessionDep
) -> Item:
    """
    Get specific item by ID.

    Args:
        item_id: Item identifier
        session: Database session (injected)

    Returns:
        Item: Item object
    """
    return example_controller.get_item_by_id(session, item_id)

@router.post("/", response_model=Item, status_code=201)
def create_item(
    item_data: ItemCreate,
    session: SessionDep
) -> Item:
    """
    Create new item.

    Args:
        item_data: Item creation data
        session: Database session (injected)

    Returns:
        Item: Created item object
    """
    return example_controller.create_item(session, item_data)

@router.patch("/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    session: SessionDep
) -> Item:
    """
    Update existing item (partial update supported).

    Args:
        item_id: Item identifier
        item_data: Updated item data
        session: Database session (injected)

    Returns:
        Item: Updated item object
    """
    return example_controller.update_item(session, item_id, item_data)

@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    session: SessionDep
) -> dict:
    """
    Delete item.

    Args:
        item_id: Item identifier
        session: Database session (injected)

    Returns:
        dict: Success message
    """
    return example_controller.delete_item(session, item_id)
'''
        write_file(f"{project_name}/src/routers/example_router.py", example_router_content)

    # Generate main.py
    main_content = f'''"""
FastAPI application entry point.
Initializes database connection and registers routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.lib.db_connect import DBConfig
from src.lib.env_config import Config

# Import routers (add your routers here)
{'from src.routers import example_router' if include_examples else ''}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events for database connection.
    """
    # Startup
    print("=" * 50)
    print(f"🚀 Starting {{Config.APP_NAME}}...")
    print("=" * 50)

    try:
        # Initialize database
        db_url = Config.get_database_url()
        db = DBConfig(url=db_url, echo=Config.DEBUG)
        db.open_connection()
        db.create_tables()

        # Store db instance in app state for session dependency
        app.state.db_init = db

        print("=" * 50)
        print(f"✓ {{Config.APP_NAME}} started successfully")
        print(f"  Version: {{Config.APP_VERSION}}")
        print(f"  Debug Mode: {{Config.DEBUG}}")
        print(f"  Docs: http://localhost:8000/docs")
        print("=" * 50)

    except Exception as e:
        print(f"✗ Failed to start application: {{e}}")
        raise

    yield

    # Shutdown
    print("=" * 50)
    print("🛑 Shutting down application...")
    db.close_connection()
    print("✓ Application shut down successfully")
    print("=" * 50)

# Initialize FastAPI application
app = FastAPI(
    title=Config.APP_NAME,
    version=Config.APP_VERSION,
    description="FastAPI backend with SQLModel ORM and SQL database support",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (add your routers here)
{'app.include_router(example_router.router)' if include_examples else ''}

# Root endpoint
@app.get("/", tags=["Health"])
def root():
    """
    Root endpoint - health check.

    Returns basic application information and health status.
    """
    return {{
        "status": "healthy",
        "app": Config.APP_NAME,
        "version": Config.APP_VERSION,
        "message": "API is running. Visit /docs for API documentation."
    }}

@app.get("/health", tags=["Health"])
def health_check():
    """
    Detailed health check endpoint.

    Returns detailed application health information.
    """
    return {{
        "status": "healthy",
        "database": "connected",
        "app_name": Config.APP_NAME,
        "version": Config.APP_VERSION
    }}
'''
    write_file(f"{project_name}/main.py", main_content)

    # Generate .env.example
    env_example_content = '''# ============================================
# APPLICATION CONFIGURATION
# ============================================
APP_NAME=FastAPI Backend
APP_VERSION=1.0.0
DEBUG=False

# ============================================
# DATABASE CONFIGURATION
# ============================================
# Supported drivers:
#   - PostgreSQL: postgresql+psycopg2
#   - MySQL: mysql+pymysql
#   - SQL Server: mssql+pyodbc
#   - SQLite: sqlite (no username/password/host needed)

DB_DRIVER=postgresql+psycopg2
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database

# Optional: For SQL Server ODBC
# DB_DRIVER_ODBC=ODBC Driver 17 for SQL Server

# ============================================
# AUTHENTICATION CONFIGURATION
# ============================================
BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================
# DATABASE EXAMPLES
# ============================================

# PostgreSQL (Local)
# DB_DRIVER=postgresql+psycopg2
# DB_USERNAME=postgres
# DB_PASSWORD=postgres
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=myapp_db

# PostgreSQL (Neon)
# DB_DRIVER=postgresql+psycopg2
# DB_USERNAME=neon_user
# DB_PASSWORD=neon_password
# DB_HOST=ep-xxx-xxx.us-east-2.aws.neon.tech
# DB_PORT=5432
# DB_NAME=neondb

# MySQL
# DB_DRIVER=mysql+pymysql
# DB_USERNAME=root
# DB_PASSWORD=root
# DB_HOST=localhost
# DB_PORT=3306
# DB_NAME=myapp_db

# SQL Server
# DB_DRIVER=mssql+pyodbc
# DB_USERNAME=sa
# DB_PASSWORD=YourPassword123
# DB_HOST=localhost
# DB_PORT=1433
# DB_NAME=myapp_db
# DB_DRIVER_ODBC=ODBC Driver 17 for SQL Server

# SQLite (file-based, no host/user/password needed)
# DB_DRIVER=sqlite
# DB_NAME=myapp
'''
    write_file(f"{project_name}/.env.example", env_example_content)

    # Generate .gitignore
    gitignore_content = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation docs/
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# FastAPI / uvicorn
uvicorn.log
access.log
error.log

# Environment variables
.env

# Database files
*.db
*.db-journal

# Logs
logs/
*.log

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
'''
    write_file(f"{project_name}/.gitignore", gitignore_content)

    # Generate pyproject.toml
    pyproject_content = f'''[project]
name = "{project_name}"
version = "0.1.0"
description = "FastAPI backend with SQLModel ORM and SQL database support"
requires-python = ">={python_version}"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "sqlmodel",
    "python-dotenv",
    "pyjwt",
    # Database drivers (install based on your database)
    "psycopg2-binary",  # PostgreSQL
    # "pymysql",         # MySQL
    # "pyodbc",          # SQL Server
]

[tool.uv]
dev-dependencies = [
    "pytest",
    "httpx",
    "pytest-asyncio",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
'''
    write_file(f"{project_name}/pyproject.toml", pyproject_content)

    # Generate README.md
    readme_content = f'''# {project_name}

A production-ready FastAPI backend with SQLModel ORM, supporting any SQL database.

## 🎯 Features

- ✨ **Clean Architecture**: Separated concerns (models, controllers, routers)
- 🗄️ **Universal Database Support**: PostgreSQL, MySQL, SQL Server, SQLite, Neon, etc.
- 🔄 **SQLModel ORM**: Type-safe database operations with Pydantic validation
- 🏗️ **Scalable Structure**: Ready for any domain (e-commerce, blog, inventory, etc.)
- 📝 **Comprehensive Documentation**: Detailed docstrings and examples
- 🧪 **Error Handling**: Custom exceptions and proper error responses
- 🔒 **Type Safety**: Full type hints throughout the codebase
- 🚀 **Production Ready**: Lifespan management, CORS, health checks

## 📁 Project Structure

```
{project_name}/
├── src/
│   ├── models/
│   │   ├── base.py (base model with common fields)
│   │   └── example_model.py (if include_examples=true)
│   ├── controllers/
│   │   └── example_controller.py (if include_examples=true)
│   ├── routers/
│   │   └── example_router.py (if include_examples=true)
│   └── lib/
│       ├── db_connect.py (database connection manager)
│       ├── env_config.py (environment configuration)
│       ├── session.py (session dependency)
│       └── exceptions.py (custom exceptions)
├── tests/
│   └── test_example.py (if include_examples=true)
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── main.py
```

## 🚀 Quick Start

1. **Clone or generate this project**

2. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   # or if using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run the application**:
   ```bash
   uvicorn main:app --reload
   # or
   python -m uvicorn main:app --reload
   ```

5. **Access the application**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 🛠️ Configuration

The application uses environment variables for configuration:

- `APP_NAME`: Application name (default: "FastAPI Backend")
- `APP_VERSION`: Application version (default: "1.0.0")
- `DEBUG`: Enable debug mode (default: "False")
- `DB_DRIVER`: Database driver (default: "postgresql+psycopg2")
- `DB_USERNAME`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host (default: "localhost")
- `DB_PORT`: Database port (default: "5432")
- `DB_NAME`: Database name (default: "database")

## 🧪 Running Tests

```bash
pytest
```

## 📚 Database Support

This project supports multiple SQL databases through SQLAlchemy:

- **PostgreSQL**: `postgresql+psycopg2://user:pass@host:5432/db`
- **MySQL**: `mysql+pymysql://user:pass@host:3306/db`
- **SQL Server**: `mssql+pyodbc://user:pass@host:1433/db?driver=...`
- **SQLite**: `sqlite:///./database.db`
- **Neon**: `postgresql+psycopg2://user:pass@neon-host/db`

## 🏗️ Architecture

The project follows a clean architecture pattern:

- **Models** (`src/models/`): Define data structures and schemas
- **Controllers** (`src/controllers/`): Handle business logic
- **Routers** (`src/routers/`): Define API endpoints
- **Lib** (`src/lib/`): Shared utilities (database, config, exceptions)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the terms described in LICENSE.txt.
'''
    write_file(f"{project_name}/README.md", readme_content)

    # Generate example test file if requested
    if include_examples:
        test_content = '''"""
Example tests for the FastAPI backend.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "version" in data

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

# Add more tests as needed for your specific endpoints
'''
        write_file(f"{project_name}/tests/test_example.py", test_content)

    print(f"FastAPI backend project '{project_name}' generated successfully!")
    print(f"Project structure created with the following features:")
    print(f"  - Clean architecture with separation of concerns")
    print(f"  - SQLModel ORM with base models and timestamp mixins")
    print(f"  - Database connection manager with session handling")
    print(f"  - Environment configuration loader with JWT settings")
    print(f"  - Custom exception classes")
    print(f"  - Authentication middleware for JWT token verification")
    print(f"  - Example models/controllers/routers (as requested)")
    print(f"  - Proper documentation and configuration files")
    print(f"  - Ready for any SQL database (PostgreSQL, MySQL, SQL Server, SQLite, etc.)")

def main():
    parser = argparse.ArgumentParser(description="Generate a FastAPI backend with SQLModel ORM")
    parser.add_argument("--project-name", type=str, default="backend", help="Name of the backend project")
    parser.add_argument("--database-type", type=str, default="postgresql",
                       choices=["postgresql", "mysql", "sqlserver", "sqlite", "neon"],
                       help="Database type hint for configuration")
    parser.add_argument("--include-examples", action="store_true", default=True,
                       help="Include example model/controller/router as reference")
    parser.add_argument("--no-examples", action="store_false", dest="include_examples",
                       help="Do not include example model/controller/router")
    parser.add_argument("--python-version", type=str, default="3.11",
                       help="Minimum Python version (default: 3.11)")

    args = parser.parse_args()

    generate_backend(
        project_name=args.project_name,
        database_type=args.database_type,
        include_examples=args.include_examples,
        python_version=args.python_version
    )

if __name__ == "__main__":
    main()