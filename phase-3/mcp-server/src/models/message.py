"""
Task model for task management.

This model represents a user's task with attributes and completion status.
"""
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, Optional, List
from src.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from src.models.user import User

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
class MessageBase(SQLModel):
    """
    Base schema for Message with common fields.
    Used for validation in create/update operations.
    """
    
    user_id: str = Field(
        foreign_key="user.id",
        description="Foreign key linking to the owning user"
    )
    conversation_id: int = Field(
        foreign_key="conversation.id",
        description="Foreign key linking to the owning conversation"
    )
    role: Role = Field(
        description="Role of the message sender (e.g., user, assistant)"
    )
    content:str = Field(
        description="Content of the message")


class MessageCreate(MessageBase):
    """
    Schema for creating new messages.
    Inherits all fields from MessageBase.
    """
    pass


class MessageUpdate(SQLModel):
    """
    Schema for updating existing messages.
    All fields are optional to allow partial updates.
    """
    role: Optional[Role] = Field(default=None, description="Role of the message sender (e.g., user, assistant)")
    content: Optional[str] = Field(default=None, max_length=2000)
    is_completed: Optional[bool] = Field(default=None)


class Message(MessageBase, TimestampMixin, table=True):
    """
    Message database model for message management.

    Represents a user's message with attributes and completion status.
    Inherits from:
        - MessageBase: Business logic fields
        - BaseModel: Common fields (id, etc.)
        - TimestampMixin: Timestamp fields (created_at, updated_at)

    Attributes:
        id: Primary key (from BaseModel)
        role: Role of the message sender (required)
        content: Content of the message (optional)
        is_completed: Flag indicating if message is completed (default: False)
        user_id: Foreign key linking to the owning user
        created_at: Creation timestamp (from TimestampMixin)
        updated_at: Last update timestamp (from TimestampMixin)
        user: Relationship to the owning User (back_populates="messages")
    """
    __tablename__ = "message"  # Explicit table name
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Primary key"
    )
    # Relationship to User model
    user: Optional["User"] = Relationship(back_populates="messages")