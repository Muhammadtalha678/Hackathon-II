"""
Example router template for FastAPI SQLModel backend.
Use this as a reference when creating your own routers.
"""
from fastapi import APIRouter, Query
from src.lib.session import SessionDep
from src.models.{model_name} import {ModelName}, {ModelName}Create, {ModelName}Update
from src.controllers import {model_name}_controller
from typing import List

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/{model_name}s",
    tags=["{ModelName}s"]
)

@router.get("/", response_model=List[{ModelName}])
def list_{model_name}s(
    session: SessionDep,
    skip: int = Query(default=0, ge=0, description="Number of {model_name}s to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of {model_name}s to return")
) -> List[{ModelName}]:
    """
    List all {model_name}s with pagination.

    Args:
        session: Database session (injected)
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List[{ModelName}]: List of {model_name}s
    """
    return {model_name}_controller.get_all_{model_name}s(session, skip=skip, limit=limit)

@router.get("/{model_name}_id", response_model={ModelName})
def get_{model_name}(
    {model_name}_id: int,
    session: SessionDep
) -> {ModelName}:
    """
    Get specific {model_name} by ID.

    Args:
        {model_name}_id: {ModelName} identifier
        session: Database session (injected)

    Returns:
        {ModelName}: {ModelName} object
    """
    return {model_name}_controller.get_{model_name}_by_id(session, {model_name}_id)

@router.post("/", response_model={ModelName}, status_code=201)
def create_{model_name}(
    {model_name}_data: {ModelName}Create,
    session: SessionDep
) -> {ModelName}:
    """
    Create new {model_name}.

    Args:
        {model_name}_data: {ModelName} creation data
        session: Database session (injected)

    Returns:
        {ModelName}: Created {model_name} object
    """
    return {model_name}_controller.create_{model_name}(session, {model_name}_data)

@router.patch("/{model_name}_id", response_model={ModelName})
def update_{model_name}(
    {model_name}_id: int,
    {model_name}_data: {ModelName}Update,
    session: SessionDep
) -> {ModelName}:
    """
    Update existing {model_name} (partial update supported).

    Args:
        {model_name}_id: {ModelName} identifier
        {model_name}_data: Updated {model_name} data
        session: Database session (injected)

    Returns:
        {ModelName}: Updated {model_name} object
    """
    return {model_name}_controller.update_{model_name}(session, {model_name}_id, {model_name}_data)

@router.delete("/{model_name}_id")
def delete_{model_name}(
    {model_name}_id: int,
    session: SessionDep
) -> dict:
    """
    Delete {model_name}.

    Args:
        {model_name}_id: {ModelName} identifier
        session: Database session (injected)

    Returns:
        dict: Success message
    """
    return {model_name}_controller.delete_{model_name}(session, {model_name}_id)