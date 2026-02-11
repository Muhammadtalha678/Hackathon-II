from sqlmodel import select
from src.models.conversation import Conversation
def get_or_create_conversation(session,user_id:str):
    statement = select(Conversation).where(Conversation.user_id == user_id)
    conv = session.exec(statement).first()

    if not conv:
        conv = Conversation(user_id=user_id)
        session.add(conv)
        session.commit()
        session.refresh(conv)
    
    history = [
        {"role":message.role, "content":message.content}
        for message in conv.messages
    ]
    
    return history,conv.id