"""
Example model template for FastAPI SQLModel backend.
Use this as a reference when creating your own models.
"""
from sqlmodel import Field
from typing import Optional
from src.models.base import BaseModel, TimestampMixin

class {ModelName}Base(SQLModel):
    """
    Base schema for {ModelName} with common fields.
    Used for validation in create/update operations.
    """
    name: str = Field(
        min_length=1,
        max_length=200,
        index=True,
        description="{ModelName} name"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="{ModelName} description"
    )


class {ModelName}Create({ModelName}Base):
    """
    Schema for creating new {ModelName} instances.
    Inherits all fields from {ModelName}Base.
    """
    pass


class {ModelName}Update(SQLModel):
    """
    Schema for updating existing {ModelName} instances.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class {ModelName}({ModelName}Base, BaseModel, TimestampMixin, table=True):
    """
    {ModelName} database model.

    Replace this with your actual domain model.

    Inherits from:
        - {ModelName}Base: Business logic fields
        - BaseModel: Common fields (id, etc.)
        - TimestampMixin: Timestamp fields (created_at, updated_at)

    Attributes:
        id: Primary key (from BaseModel)
        name: {ModelName} name
        description: {ModelName} description
        created_at: Creation timestamp (from TimestampMixin)
        updated_at: Last update timestamp (from TimestampMixin)
    """
    __tablename__ = "{model_name}s"  # Explicit table name