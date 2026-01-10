"""
User model for authentication and user management.

This model represents a registered user with authentication information.
Frontend authentication is handled by Better Auth, backend only verifies JWT tokens.
"""
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, Optional, List
from src.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from src.models.task import Task


class UserBase(SQLModel):
    """
    Base schema for User with common fields.
    Used for validation in create/update operations.
    """
    # id: str = Field(primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    emailVerified: bool
    image: Optional[str] = None



class UserCreate(UserBase):
    """
    Schema for creating new users.
    Inherits all fields from UserBase.
    """
    pass


class UserUpdate(SQLModel):
    """
    Schema for updating existing users.
    All fields are optional to allow partial updates.
    """
    email: Optional[str] = Field(default=None, max_length=255)
    is_active: Optional[bool] = Field(default=None)


class User(UserBase, BaseModel, TimestampMixin, table=True):
    """
    User database model for authentication.

    Represents a registered user with authentication information.
    Frontend authentication is handled by Better Auth, backend only verifies JWT tokens.
    Inherits from:
        - UserBase: Business logic fields
        - BaseModel: Common fields (id, etc.)
        - TimestampMixin: Timestamp fields (created_at, updated_at)

    Attributes:
        id: Primary key (from BaseModel)
        email: User's email address for identification
        is_active: Flag indicating if user account is active
        created_at: Creation timestamp (from TimestampMixin)
        updated_at: Last update timestamp (from TimestampMixin)
        tasks: List of associated Task objects (back_populates="user")
    """
    __tablename__ = "user"  # Explicit table name

    # Relationship to Task model
    tasks: List["Task"] = Relationship(back_populates="user")