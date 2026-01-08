"""
Auth controller template for FastAPI SQLModel backend with JWT authentication.
Use this as a reference when creating your own authentication controller.
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status

from sqlmodel import select
from src.models.user_model import User, UserCreate
from src.lib.session import SessionDep
from src.lib.env_config import Config
from src.lib.exceptions import ValidationException, ConflictException, DatabaseException


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT access token.

    Args:
        data: Data to encode in the token (typically user info like email)
        expires_delta: Token expiration time (defaults to config value)

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, Config.BETTER_AUTH_SECRET, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt


def authenticate_user(session: SessionDep, email: str, password: str) -> Optional[User]:
    """
    Authenticate user with email and password.
    This is a placeholder - you'll need to implement password verification based on your User model.

    Args:
        session: Database session
        email: User email
        password: Plain text password (in real implementation, verify against hashed password)

    Returns:
        User: Authenticated user if credentials are valid, None otherwise
    """
    # This is a placeholder - implement based on your actual User model with password hashing
    user = session.exec(select(User).where(User.email == email)).first()
    # In a real implementation, you would verify the password here
    # if user and verify_password(password, user.hashed_password):
    #     return user
    if user:
        return user
    return None


def get_user_by_email(session: SessionDep, email: str) -> Optional[User]:
    """
    Get user by email.

    Args:
        session: Database session
        email: User email

    Returns:
        User: User object if found, None otherwise
    """
    try:
        user = session.exec(select(User).where(User.email == email)).first()
        return user
    except Exception as e:
        raise DatabaseException(f"Failed to retrieve user: {str(e)}")


def get_user_by_id(session: SessionDep, user_id: int) -> Optional[User]:
    """
    Get user by ID.

    Args:
        session: Database session
        user_id: User identifier

    Returns:
        User: User object if found, None otherwise
    """
    try:
        user = session.get(User, user_id)
        return user
    except Exception as e:
        raise DatabaseException(f"Failed to retrieve user: {str(e)}")