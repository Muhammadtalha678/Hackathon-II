from fastapi import APIRouter, Depends, Path, HTTPException, Request, status
from typing import Annotated
from src.lib.helper import AuthContext
from src.lib.session import SessionDep
from src.controllers import chat_controller
from src.lib.auth import get_current_user
from src.models.user import User
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/{user_id}",
    tags=["Chat"]
)

UserID = Annotated[str, Path(min_length=1,description="The user ID")]

class Chat(BaseModel):
    query: str

@router.post("/chat", status_code=200)
async def chat_endpoint(
    request:Request,
    session: SessionDep,
    user_id: UserID,
    chat: Chat,
    auth: AuthContext = Depends(get_current_user),
): 
    
    # print(auth)
    # Verify that the user_id in the URL matches the authenticated user
    if auth.user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    agent_config = request.app.state.agent_config

    return await chat_controller.create_chat_for_user(token=auth.token,session=session, query=chat.query, user_id=user_id,agent_config=agent_config)