"""
Session dependency for FastAPI route handlers.
Provides reusable database session through dependency injection.
"""
from fastapi import Request, Depends
from typing import Annotated
from sqlmodel import Session

def get_session_from_request(request: Request):
    """
    Get database session from application state.

    Args:
        request: FastAPI request object containing app state

    Yields:
        Session: Database session instance

    Example Usage in Router:
        @router.get("/items")
        def get_items(session: SessionDep):
            items = session.exec(select(Item)).all()
            return items
    """
    db = request.app.state.db_init
    yield from db.get_session()

# Type annotation for session dependency injection
# Use this in all route handlers that need database access
SessionDep = Annotated[Session, Depends(get_session_from_request)]
