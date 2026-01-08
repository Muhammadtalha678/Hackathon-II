"""
Auth router template for FastAPI SQLModel backend with JWT authentication.
Use this as a reference when creating your own authentication router.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from datetime import timedelta

from src.lib.session import SessionDep
from src.lib.auth import verify_token_middleware, get_current_user
from src.models.user_model import User
from src.controllers import auth_controller
from src.lib.exceptions import ValidationException

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login")
def login_user(
    request: Request,
    email: str,
    password: str,
    session: SessionDep
):
    """
    Authenticate user and return JWT token.

    Args:
        request: FastAPI request object
        email: User email
        password: User password
        session: Database session (injected)

    Returns:
        dict: Access token and token type
    """
    user = auth_controller.authenticate_user(session, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)  # You can make this configurable
    access_token = auth_controller.create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )

    # Set token in cookie as well
    response = Response()
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=1800  # 30 minutes in seconds
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }


@router.post("/logout")
def logout_user(response: Response):
    """
    Logout user by clearing the access token cookie.

    Args:
        response: FastAPI response object

    Returns:
        dict: Success message
    """
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}


@router.get("/me")
def get_current_user_info(
    current_user: Annotated[User, Depends(verify_token_middleware)]
):
    """
    Get current authenticated user information.

    Args:
        current_user: Authenticated user (injected via middleware)

    Returns:
        dict: User information
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "is_active": current_user.is_active
    }


@router.get("/protected")
def protected_route(
    current_user: Annotated[User, Depends(verify_token_middleware)]
):
    """
    Example of a protected route that requires authentication.

    Args:
        current_user: Authenticated user (injected via middleware)

    Returns:
        dict: Success message with user info
    """
    return {
        "message": "This is a protected route",
        "user_email": current_user.email
    }