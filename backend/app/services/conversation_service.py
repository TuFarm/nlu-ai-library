from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.schema import Conversation, ConversationMessage, UserSession
from app.services.interaction_service import record_event


def start_conversation(db: Session, session_id: UUID | None, user_id: UUID | None) -> Conversation:
    conversation = Conversation(session_id=session_id, user_id=user_id, started_at=datetime.now(UTC), status="active")
    db.add(conversation); db.commit(); db.refresh(conversation)
    return conversation


def save_message(db: Session, conversation: Conversation, sender_type: str, message_text: str,
                 input_method: str) -> ConversationMessage:
    message = ConversationMessage(conversation_id=conversation.id, sender_type=sender_type,
        message_text=message_text, input_method=input_method, message_time=datetime.now(UTC))
    db.add(message); db.flush()
    if sender_type.upper() == "USER" and conversation.session_id:
        session = db.get(UserSession, conversation.session_id)
        record_event(db, event_type="QUESTION_ASKED", session_id=conversation.session_id,
            user_id=conversation.user_id, device_id=session.device_id if session else None,
            input_method=input_method, content_summary=message_text[:500])
    db.commit(); db.refresh(message)
    return message
