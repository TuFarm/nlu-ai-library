from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.core.responses import success_response
from app.models.schema import Conversation, User, UserSession
from app.schemas.conversation import ConversationMessageCreate, ConversationStart
from app.services.conversation_service import save_message, start_conversation

router = APIRouter()


@router.post("/start")
def start(payload: ConversationStart, db: Session = Depends(get_db)) -> dict:
    if payload.session_id and db.get(UserSession, payload.session_id) is None:
        raise AppError(404, "SESSION_NOT_FOUND", "Không tìm thấy phiên kiosk.")
    if payload.user_id and db.get(User, payload.user_id) is None:
        raise AppError(404, "USER_NOT_FOUND", "Không tìm thấy người dùng.")
    conversation = start_conversation(db, payload.session_id, payload.user_id)
    return success_response({"conversation_id": str(conversation.id), "status": conversation.status})


@router.post("/{conversation_id}/messages")
def create_message(conversation_id: UUID, payload: ConversationMessageCreate, db: Session = Depends(get_db)) -> dict:
    conversation = db.get(Conversation, conversation_id)
    if conversation is None: raise AppError(404, "CONVERSATION_NOT_FOUND", "Không tìm thấy hội thoại.")
    message = save_message(db, conversation, payload.sender_type, payload.message_text, payload.input_method)
    return success_response({"id": str(message.id), "conversation_id": str(conversation_id), "sender_type": message.sender_type,
        "message_text": message.message_text, "input_method": message.input_method, "message_time": message.message_time.isoformat()})
