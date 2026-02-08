"""
MCP server application entry point.
Initializes database connection and registers routes.
"""
from http.client import HTTPException
import logging
from typing import List, Optional
from fastmcp import FastMCP,Context

import jwt
from contextlib import asynccontextmanager

from sqlmodel import Session, select
from src.lib.auth_middleware import AuthMiddleware
from src.models.user import User
from src.models.task import Task,TaskRead,TaskCreate
from src.models.conversation import Conversation
from src.models.message import Message
from src.lib.db_connect import DBConfig
from src.lib.env_config import Config
from src.lib.lifespan import app_lifespan
from fastmcp.exceptions import ToolError


# Initialize FastAPI application

mcp = FastMCP(
    name=Config.APP_NAME,
    lifespan=app_lifespan,
    middleware=[AuthMiddleware()],
    stateless_http=True
)


@mcp.tool(name="list_tasks", description="Retrieve tasks from the database")
def list_tasks(user_id:str,status: str = "all",context:Context = None)->List[TaskRead]:
    """
    Tool to list tasks from the database with optional status filtering.
    """
    user = context.request_context.request.state.user
    print(user.id)
    if user_id != user.id:
        raise ToolError(f"Security Alert: You cannot access tasks for user {user_id}")
    db = context.request_context.lifespan_context.get("db")
    try:
        with next(db.get_session()) as session:
            statement = select(Task).where(Task.user_id == user.id)
            if status == "completed":
                statement = statement.where(Task.is_completed == True)
            elif status == "pending":
                statement = statement.where(Task.is_completed == False)
            tasks = session.exec(statement).all()
            return tasks
    except Exception as e:
        print(f"Database Error: {e}")
        raise ToolError(f"Failed to retrieve tasks for user {user.id}: {str(e)}")

@mcp.tool(name="add_task", description="Create a new task for the authenticated user.")
def add_task(
    task:TaskCreate, 
    context: Context
):
    """
    Tool to create a new task in the database.
    """
    
    auth_user = context.request_context.request.state.user
    
    
    if task.user_id != auth_user.id:
        raise ToolError(f"Unauthorized: You cannot add tasks for user {task.user_id}")

    
    db = context.request_context.lifespan_context.get("db")
    
    try:
        with next(db.get_session()) as session:
            
            new_task = Task(**task.model_dump())
            
            session.add(new_task)
            session.commit()
            session.refresh(new_task) 
            
            
            return {
                "task_id": new_task.id,
                "status": "created",
                "title": new_task.title
            }

    except Exception as e:
        print(f"Database Error: {e}")
        raise ToolError(f"Failed to create task: {str(e)}")


@mcp.tool(name="complete_task", description="Mark a task as complete")
def complete_task(user_id: str, task_id: int, context: Context):
    auth_user = context.request_context.request.state.user
    if user_id != auth_user.id:
        raise ToolError("Unauthorized access")

    db = context.request_context.lifespan_context.get("db")
    try:
        with next(db.get_session()) as session:
            # Sirf woh task uthao jo is user ka ho
            task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == auth_user.id)).first()
            if not task:
                raise ToolError(f"Task {task_id} not found or not owned by you")
            
            task.is_completed = True
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {"task_id": task.id, "status": "completed", "title": task.title}
    except Exception as e:
        raise ToolError(f"Update failed: {str(e)}")



@mcp.tool(name="delete_task", description="Remove a task from the list")
def delete_task(user_id: str, task_id: int, context: Context):
    auth_user = context.request_context.request.state.user
    if user_id != auth_user.id:
        raise ToolError("Unauthorized access")

    db = context.request_context.lifespan_context.get("db")
    try:
        with next(db.get_session()) as session:
            task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == auth_user.id)).first()
            if not task:
                raise ToolError(f"Task {task_id} not found")
            
            session.delete(task)
            session.commit()
            
            return {"task_id": task_id, "status": "deleted", "title": task.title}
    except Exception as e:
        raise ToolError(f"Deletion failed: {str(e)}")


@mcp.tool(name="update_task", description="Modify task title or description")
def update_task(
    user_id: str, 
    task_id: int, 
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    context: Context = None
):
    auth_user = context.request_context.request.state.user
    if user_id != auth_user.id:
        raise ToolError("Unauthorized access")

    db = context.request_context.lifespan_context.get("db")
    try:
        with next(db.get_session()) as session:
            # 1. Pehle purana task dhundein
            task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == auth_user.id)).first()
            if not task:
                raise ToolError(f"Task {task_id} not found")
            
            # 2. DUPLICATE CHECK: Agar title change ho raha hai, toh check karein kahin naya title pehle se toh nahi?
            if title is not None and title != task.title:
                existing_task = session.exec(
                    select(Task).where(Task.title == title, Task.user_id == auth_user.id)
                ).first()
                if existing_task:
                    raise ToolError(f"Task with title '{title}' already exists for your account")

            # 3. Update logic
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
                
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {"task_id": task.id, "status": "updated", "title": task.title}
            
    except ToolError as te:
        # ToolError ko as-is aage bhejien taake client ko sahi message mile
        raise te
    except Exception as e:
        raise ToolError(f"Update failed: {str(e)}")



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    mcp.run(transport="http", host="0.0.0.0", port=port)