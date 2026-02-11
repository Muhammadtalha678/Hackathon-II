"""
Custom exception classes for the application.
Provides structured error handling across the application.
"""
from fastapi import HTTPException, status

class DatabaseException(HTTPException):
    """Base exception for database-related errors."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {detail}"
        )

class NotFoundException(HTTPException):
    """Exception for resource not found errors."""

    def __init__(self, resource: str, identifier: str | int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id '{identifier}' not found"
        )

class ValidationException(HTTPException):
    """Exception for validation errors."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {detail}"
        )

class ConflictException(HTTPException):
    """Exception for resource conflict errors (e.g., duplicate entries)."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Conflict: {detail}"
        )
