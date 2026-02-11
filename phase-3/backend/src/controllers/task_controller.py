"""
Task controller for handling task-related business logic.

This controller implements the business logic for task operations
including listing, creating, updating, deleting, and toggling completion.
All operations enforce user-specific access control.
"""
from sqlmodel import select
from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User
from src.lib.session import SessionDep
from src.lib.exceptions import NotFoundException, DatabaseException
from typing import List


def get_user_tasks(session: SessionDep, user_id: int) -> List[Task]:
    """
    Retrieve all tasks for a specific user.

    Args:
        session: Database session
        user_id: User identifier to filter tasks

    Returns:
        List[Task]: List of tasks belonging to the user

    Raises:
        DatabaseException: If query fails
    """
    try:
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return list(tasks)
    except Exception as e:
        raise DatabaseException(f"Failed to retrieve tasks for user {user_id}: {str(e)}")


def get_task_by_id_and_user(session: SessionDep, task_id: int, user_id: int) -> Task:
    """
    Retrieve a specific task for a specific user.

    Args:
        session: Database session
        task_id: Task identifier
        user_id: User identifier

    Returns:
        Task: The requested task object

    Raises:
        NotFoundException: If task not found for the user
        DatabaseException: If query fails
    """
    try:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            raise NotFoundException("Task", task_id)
        return task
    except NotFoundException:
        raise
    except Exception as e:
        raise DatabaseException(f"Failed to retrieve task {task_id} for user {user_id}: {str(e)}")


def create_task_for_user(session: SessionDep, task_data: TaskCreate, user_id: int) -> Task:
    """
    Create a new task for a specific user.

    Args:
        session: Database session
        task_data: Task creation data
        user_id: User identifier (owner of the task)

    Returns:
        Task: The created task object

    Raises:
        DatabaseException: If creation fails
    """
    try:
        # Verify the user exists
        user = session.get(User, user_id)
        if not user:
            raise NotFoundException("User", user_id)

        # Create task with the specified user_id
        task = Task.model_validate(task_data)
        task.user_id = user_id

        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except NotFoundException:
        raise
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Failed to create task for user {user_id}: {str(e)}")


def update_task_for_user(session: SessionDep, task_id: int, user_id: int, task_data: TaskUpdate) -> Task:
    """
    Update an existing task for a specific user.

    Args:
        session: Database session
        task_id: Task identifier
        user_id: User identifier
        task_data: Updated task data

    Returns:
        Task: The updated task object

    Raises:
        NotFoundException: If task not found for the user
        DatabaseException: If update fails
    """
    try:
        # Get the existing task
        task = session.get(Task, task_id)
        if not task:
            raise NotFoundException("Task", task_id)

        # Verify that the task belongs to the user
        if task.user_id != user_id:
            raise NotFoundException("Task", task_id)  # Don't reveal that task exists for another user

        # Update only provided fields
        update_data = task_data.model_dump(exclude_unset=True)
        print(update_data)
        for key, value in update_data.items():
            setattr(task, key, value)

        # Update the updated_at timestamp
        from datetime import datetime
        task.updated_at = datetime.now()
        # print(task)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except NotFoundException:
        raise
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Failed to update task {task_id} for user {user_id}: {str(e)}")


def delete_task_for_user(session: SessionDep, task_id: int, user_id: int) -> dict:
    """
    Delete a task for a specific user.

    Args:
        session: Database session
        task_id: Task identifier
        user_id: User identifier

    Returns:
        dict: Success message with deleted task details

    Raises:
        NotFoundException: If task not found for the user
        DatabaseException: If deletion fails
    """
    try:
        # Get the existing task
        task = session.get(Task, task_id)
        if not task:
            raise NotFoundException("Task", task_id)

        # Verify that the task belongs to the user
        if task.user_id != user_id:
            raise NotFoundException("Task", task_id)  # Don't reveal that task exists for another user

        session.delete(task)
        session.commit()
        return {
            "success": True,
            "message": f"Task '{task.title}' deleted successfully",
            "deleted_id": task_id
        }
    except NotFoundException:
        raise
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Failed to delete task {task_id} for user {user_id}: {str(e)}")


def toggle_task_completion(session: SessionDep, task_id: int, user_id: int) -> Task:
    """
    Toggle the completion status of a task for a specific user.

    Args:
        session: Database session
        task_id: Task identifier
        user_id: User identifier

    Returns:
        Task: The updated task object with toggled completion status

    Raises:
        NotFoundException: If task not found for the user
        DatabaseException: If update fails
    """
    try:
        # Get the existing task
        task = session.get(Task, task_id)
        if not task:
            raise NotFoundException("Task", task_id)

        # Verify that the task belongs to the user
        if task.user_id != user_id:
            raise NotFoundException("Task", task_id)  # Don't reveal that task exists for another user

        # Toggle the completion status
        task.is_completed = not task.is_completed

        # Update the updated_at timestamp
        from datetime import datetime
        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except NotFoundException:
        raise
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Failed to toggle completion for task {task_id} for user {user_id}: {str(e)}")