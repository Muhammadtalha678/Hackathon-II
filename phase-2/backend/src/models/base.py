"""
Base model with common fields and utilities.
All application models should inherit from these base classes.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

class TimestampMixin(SQLModel):
    """
    Mixin for adding timestamp fields to models.

    Provides created_at and updated_at fields for tracking
    record creation and modification times.
    """
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        nullable=False,
        description="Timestamp when record was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        nullable=False,
        description="Timestamp when record was last updated"
    )

class BaseModel(SQLModel):
    """
    Base model for all database models.

    Provides common fields and methods that all models should have.
    Inherit from this class when creating new models.
    """
    id: Optional[str] = Field(
        default=None,
        primary_key=True,
        # description="Primary key"
    )

    class Config:
        """SQLModel configuration."""
        # Add any model-wide configuration here
        pass
