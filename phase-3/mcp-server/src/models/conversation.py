"""
Task model for task management.

This model represents a user's task with attributes and completion status.
"""
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, Optional, List
from src.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.message import Message


class ConversationBase(SQLModel):
    """
    Base schema for Conversation with common fields.
    Used for validation in create/update operations.
    """
    
    user_id: str = Field(
        foreign_key="user.id",
        description="Foreign key linking to the owning user"
    )


class ConversationCreate(ConversationBase):
    """
    Schema for creating new conversations.
    Inherits all fields from ConversationBase.
    """
    pass


class ConversationUpdate(SQLModel):
    """
    Schema for updating existing conversations.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: Optional[bool] = Field(default=None)


class Conversation(ConversationBase, TimestampMixin, table=True):
    """
    Conversation database model for conversation management.

    Represents a user's conversation with attributes and completion status.
    Inherits from:
        - ConversationBase: Business logic fields
        - BaseModel: Common fields (id, etc.)
        - TimestampMixin: Timestamp fields (created_at, updated_at)

    Attributes:
        id: Primary key (from BaseModel)
        title: Conversation title/description (required)
        description: Detailed description of the conversation (optional)
        is_completed: Flag indicating if conversation is completed (default: False)
        user_id: Foreign key linking to the owning user
        created_at: Creation timestamp (from TimestampMixin)
        updated_at: Last update timestamp (from TimestampMixin)
        user: Relationship to the owning User (back_populates="conversations")
    """
    __tablename__ = "conversation"  # Explicit table name
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Primary key"
    )
    # Relationship to User model
    user: Optional["User"] = Relationship(back_populates="conversations")
    messages: Optional[List["Message"]] = Relationship(back_populates="conversations")