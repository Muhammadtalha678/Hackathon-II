"""
Task model for task management.

This model represents a user's task with attributes and completion status.
"""
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, Optional, List
from src.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from src.models.user import User


class TaskBase(SQLModel):
    """
    Base schema for Task with common fields.
    Used for validation in create/update operations.
    """
    title: str = Field(
        min_length=1,
        max_length=500,
        description="Task title/description (required)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Detailed description of the task (optional)"
    )
    is_completed: bool = Field(
        default=False,
        description="Flag indicating if task is completed"
    )
    user_id: str = Field(
        foreign_key="user.id",
        description="Foreign key linking to the owning user"
    )


class TaskCreate(TaskBase):
    """
    Schema for creating new tasks.
    Inherits all fields from TaskBase.
    """
    pass

class TaskRead(SQLModel):
    """
    Schema for reading tasks.
    """
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    user_id: str


class TaskUpdate(SQLModel):
    """
    Schema for updating existing tasks.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: Optional[bool] = Field(default=None)


class Task(TaskBase, TimestampMixin, table=True):
    """
    Task database model for task management.

    Represents a user's task with attributes and completion status.
    Inherits from:
        - TaskBase: Business logic fields
        - BaseModel: Common fields (id, etc.)
        - TimestampMixin: Timestamp fields (created_at, updated_at)

    Attributes:
        id: Primary key (from BaseModel)
        title: Task title/description (required)
        description: Detailed description of the task (optional)
        is_completed: Flag indicating if task is completed (default: False)
        user_id: Foreign key linking to the owning user
        created_at: Creation timestamp (from TimestampMixin)
        updated_at: Last update timestamp (from TimestampMixin)
        user: Relationship to the owning User (back_populates="tasks")
    """
    __tablename__ = "tasks"  # Explicit table name
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Primary key"
    )
    # Relationship to User model
    user: Optional["User"] = Relationship(back_populates="tasks")