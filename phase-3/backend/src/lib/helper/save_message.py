from sqlmodel import select
from src.models.message import Message

def save_message(session, user_id: str, conversation_id: int, role: str, content: str):
    new_message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    session.add(new_message)
    session.commit()
    # session.refresh(new_message)
    # return new_message