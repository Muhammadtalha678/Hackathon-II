"""
User model template for FastAPI SQLModel backend with authentication.
Use this as a reference when creating your own user model.
"""
from sqlmodel import Field
from typing import Optional
from src.models.base import BaseModel, TimestampMixin
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserBase(SQLModel):
    """
    Base schema for User with common fields.
    Used for validation in create/update operations.
    """
    email: str = Field(
        unique=True,
        nullable=False,
        description="User email address"
    )
    name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="User's full name"
    )
    is_active: bool = Field(
        default=True,
        description="Whether the user account is active"
    )


class UserCreate(UserBase):
    """
    Schema for creating new users.
    Includes password field which will be hashed.
    """
    password: str = Field(
        min_length=8,
        description="User password (will be hashed)"
    )


class UserUpdate(SQLModel):
    """
    Schema for updating existing users.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, unique=True)
    is_active: Optional[bool] = Field(default=None)


class User(UserBase, BaseModel, TimestampMixin, table=True):
    """
    User database model with authentication fields.

    Inherits from:
        - UserBase: Business logic fields
        - BaseModel: Common fields (id, etc.)
        - TimestampMixin: Timestamp fields (created_at, updated_at)

    Attributes:
        id: Primary key (from BaseModel)
        email: User email address
        name: User's full name
        is_active: Whether the user account is active
        hashed_password: Hashed password stored in database
        created_at: Creation timestamp (from TimestampMixin)
        updated_at: Last update timestamp (from TimestampMixin)
    """
    __tablename__ = "users"  # Explicit table name

    hashed_password: str = Field(
        nullable=False,
        description="Hashed password"
    )

    def verify_password(self, plain_password: str) -> bool:
        """
        Verify a plain password against the hashed password.

        Args:
            plain_password: Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain password.

        Args:
            password: Plain text password to hash

        Returns:
            str: Hashed password
        """
        return pwd_context.hash(password)