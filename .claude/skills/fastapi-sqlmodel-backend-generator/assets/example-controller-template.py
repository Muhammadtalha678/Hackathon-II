"""
Example controller template for FastAPI SQLModel backend.
Use this as a reference when creating your own controllers.
"""
from sqlmodel import select
from src.models.{model_name} import {ModelName}, {ModelName}Create, {ModelName}Update
from src.lib.session import SessionDep
from src.lib.exceptions import NotFoundException, DatabaseException
from typing import List, Optional

def get_all_{model_name}s(session: SessionDep, skip: int = 0, limit: int = 100) -> List[{ModelName}]:
    """
    Retrieve all {model_name}s with pagination.

    Args:
        session: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        List[{ModelName}]: List of {model_name}s

    Raises:
        DatabaseException: If query fails
    """
    try:
        statement = select({ModelName}).offset(skip).limit(limit)
        {model_name}s = session.exec(statement).all()
        return list({model_name}s)
    except Exception as e:
        raise DatabaseException(f"Failed to retrieve {model_name}s: {str(e)}")


def get_{model_name}_by_id(session: SessionDep, {model_name}_id: int) -> {ModelName}:
    """
    Retrieve specific {model_name} by ID.

    Args:
        session: Database session
        {model_name}_id: {ModelName} identifier

    Returns:
        {ModelName}: {ModelName} object

    Raises:
        NotFoundException: If {model_name} not found
        DatabaseException: If query fails
    """
    try:
        {model_name} = session.get({ModelName}, {model_name}_id)
        if not {model_name}:
            raise NotFoundException("{ModelName}", {model_name}_id)
        return {model_name}
    except NotFoundException:
        raise
    except Exception as e:
        raise DatabaseException(f"Failed to retrieve {model_name}: {str(e)}")


def create_{model_name}(session: SessionDep, {model_name}_data: {ModelName}Create) -> {ModelName}:
    """
    Create new {model_name} in database.

    Args:
        session: Database session
        {model_name}_data: {ModelName} creation data

    Returns:
        {ModelName}: Created {model_name} object

    Raises:
        DatabaseException: If creation fails
    """
    try:
        {model_name} = {ModelName}.model_validate({model_name}_data)
        session.add({model_name})
        session.commit()
        session.refresh({model_name})
        return {model_name}
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Failed to create {model_name}: {str(e)}")


def update_{model_name}(session: SessionDep, {model_name}_id: int, {model_name}_data: {ModelName}Update) -> {ModelName}:
    """
    Update existing {model_name}.

    Args:
        session: Database session
        {model_name}_id: {ModelName} identifier
        {model_name}_data: Updated {model_name} data (partial updates supported)

    Returns:
        {ModelName}: Updated {model_name} object

    Raises:
        NotFoundException: If {model_name} not found
        DatabaseException: If update fails
    """
    try:
        {model_name} = session.get({ModelName}, {model_name}_id)
        if not {model_name}:
            raise NotFoundException("{ModelName}", {model_name}_id)

        # Update only provided fields
        update_data = {model_name}_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr({model_name}, key, value)

        # Update the updated_at timestamp
        from datetime import datetime
        {model_name}.updated_at = datetime.utcnow()

        session.add({model_name})
        session.commit()
        session.refresh({model_name})
        return {model_name}
    except NotFoundException:
        raise
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Failed to update {model_name}: {str(e)}")


def delete_{model_name}(session: SessionDep, {model_name}_id: int) -> dict:
    """
    Delete {model_name} from database.

    Args:
        session: Database session
        {model_name}_id: {ModelName} identifier

    Returns:
        dict: Success message with deleted {model_name} details

    Raises:
        NotFoundException: If {model_name} not found
        DatabaseException: If deletion fails
    """
    try:
        {model_name} = session.get({ModelName}, {model_name}_id)
        if not {model_name}:
            raise NotFoundException("{ModelName}", {model_name}_id)

        session.delete({model_name})
        session.commit()
        return {
            "success": True,
            "message": f"{ModelName} '{model_name}.name}' deleted successfully",
            "deleted_id": {model_name}_id
        }
    except NotFoundException:
        raise
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Failed to delete {model_name}: {str(e)}")