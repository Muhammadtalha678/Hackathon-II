"""
Task router for handling task-related API endpoints.

This router defines the RESTful API endpoints for task management
including listing, creating, updating, deleting, and toggling completion.
All endpoints require JWT authentication and enforce user-specific access control.
"""
from fastapi import APIRouter, Depends, Path, HTTPException, status
from typing import Annotated, List
from src.lib.session import SessionDep
from src.models.task import Task, TaskCreate, TaskUpdate
from src.controllers import task_controller
from src.lib.auth import get_current_user
from src.models.user import User


# Create router with prefix and tags
router = APIRouter(
    prefix="/api/{user_id}",
    tags=["Tasks"]
)

UserID = Annotated[int, Path(gt=0,description="The user ID")]

@router.get("/tasks", response_model=List[Task])
def list_user_tasks(
    session: SessionDep,
    user_id: UserID,
    current_user: User = Depends(get_current_user),
) -> List[Task]:
    """
    List all tasks for the specified user.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        current_user: The authenticated user (from JWT token)
        session: Database session (injected)

    Returns:
        List[Task]: List of tasks belonging to the user

    Raises:
        HTTPException: If user_id in URL doesn't match authenticated user
    """
    # Verify that the user_id in the URL matches the authenticated user
    # print("current_user",current_user)
    # print("user_id",user_id)
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's tasks"
        )

    return task_controller.get_user_tasks(session, user_id)


@router.get("/tasks/{task_id}", response_model=Task)
def get_user_task(
    session: SessionDep,
    user_id:UserID,
    task_id: int = Path(..., description="The ID of the task to retrieve"),
    current_user: User = Depends(get_current_user),
) -> Task:
    """
    Get details of a specific task for the specified user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to retrieve
        current_user: The authenticated user (from JWT token)
        session: Database session (injected)

    Returns:
        Task: The requested task object

    Raises:
        HTTPException: If user_id in URL doesn't match authenticated user or task not found
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's task"
        )

    return task_controller.get_task_by_id_and_user(session, task_id, user_id)


@router.post("/tasks", response_model=Task, status_code=201)
def create_user_task(
    session: SessionDep,
    task_data: TaskCreate,
    user_id: int = Path(..., description="The ID of the user to create task for"),
    current_user: User = Depends(get_current_user),
) -> Task:
    """
    Create a new task for the specified user.

    Args:
        task_data: Task creation data
        user_id: The ID of the user to create task for
        current_user: The authenticated user (from JWT token)
        session: Database session (injected)

    Returns:
        Task: The created task object

    Raises:
        HTTPException: If user_id in URL doesn't match authenticated user
    """
    # Verify that the user_id in the URL matches the authenticated user
    print(current_user.id)
    print(user_id)
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot create task for another user"
        )

    return task_controller.create_task_for_user(session, task_data, user_id)


@router.put("/tasks/{task_id}", response_model=Task)
def update_user_task(
    task_data: TaskUpdate,
    session: SessionDep,
    user_id:UserID,
    task_id: int = Path(..., description="The ID of the task to update"),
    current_user: User = Depends(get_current_user),
) -> Task:
    """
    Update a specific task for the specified user.

    Args:
        task_data: Updated task data
        user_id: The ID of the user
        task_id: The ID of the task to update
        current_user: The authenticated user (from JWT token)
        session: Database session (injected)

    Returns:
        Task: The updated task object

    Raises:
        HTTPException: If user_id in URL doesn't match authenticated user or task not found
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot update another user's task"
        )

    return task_controller.update_task_for_user(session, task_id, user_id, task_data)


@router.delete("/tasks/{task_id}")
def delete_user_task(
    session: SessionDep,
    user_id:UserID,
    task_id: int = Path(..., description="The ID of the task to delete"),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Delete a specific task for the specified user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to delete
        current_user: The authenticated user (from JWT token)
        session: Database session (injected)

    Returns:
        dict: Success message with deleted task details

    Raises:
        HTTPException: If user_id in URL doesn't match authenticated user or task not found
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot delete another user's task"
        )

    return task_controller.delete_task_for_user(session, task_id, user_id)


@router.patch("/tasks/{task_id}/complete", response_model=Task)
def toggle_task_completion(
    session: SessionDep,
    user_id:UserID,
    task_id: int = Path(..., description="The ID of the task to update"),
    current_user: User = Depends(get_current_user),
) -> Task:
    """
    Toggle the completion status of a specific task for the specified user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        current_user: The authenticated user (from JWT token)
        session: Database session (injected)

    Returns:
        Task: The updated task object with toggled completion status

    Raises:
        HTTPException: If user_id in URL doesn't match authenticated user or task not found
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot update another user's task"
        )

    return task_controller.toggle_task_completion(session, task_id, user_id)