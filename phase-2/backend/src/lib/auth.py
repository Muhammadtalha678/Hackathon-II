"""
Authentication middleware and utilities using JWT tokens.
Verifies access tokens from either headers or cookies.
"""
from fastapi import HTTPException, Request, status, Depends
import jwt
from typing import Optional
from sqlmodel import Session, select
from src.lib.public_key_Ed25519 import load_eddsa_public_key
from src.models.user import User
from src.lib.env_config import Config
from src.lib.session import SessionDep
from src.lib.exceptions import ValidationException


def verify_token_middleware(
    request: Request,
    session: SessionDep
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
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token header"
        )
     # Get JWKS from app state
    jwks = request.app.state.jwks
    key = next((k for k in jwks if k["kid"] == kid), None)
    print(key)
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Public key for token not found"
        )
    
    public_key_obj = load_eddsa_public_key(key)
    print("public_key_obj",public_key_obj)
    # Decode and verify the token
    try:
        decoded_data = jwt.decode(
            token,
            public_key_obj,
            algorithms=[key['alg']],
            issuer= "http://localhost:3000",
            audience= "http://localhost:3000"
        )
        email = decoded_data["email"]
        print(decoded_data)
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
        print(email)
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
    session: SessionDep
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
