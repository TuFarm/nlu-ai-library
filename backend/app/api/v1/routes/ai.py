from datetime import UTC, datetime
from time import perf_counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.core.responses import success_response
from app.models.schema import AIRequest, AIResponse, Conversation, ConversationMessage, UserSession
from app.schemas.ai import AIRuntimeRequest, AIAnswerRequest
from app.services.ai_service import AIService
from app.services.conversation_service import save_message
from app.services.interaction_service import record_event

router = APIRouter()


@router.post("/answer")
def runtime_answer(payload: AIRuntimeRequest, db: Session = Depends(get_db)) -> dict:
    conversation = db.get(Conversation, payload.conversation_id)
    if conversation is None: raise AppError(404, "CONVERSATION_NOT_FOUND", "Không tìm thấy hội thoại.")
    user_message = save_message(db, conversation, "USER", payload.message_text, "TEXT")
    started = perf_counter(); answer = AIService().answer(payload.message_text); latency = int((perf_counter() - started) * 1000)
    request = AIRequest(conversation_id=conversation.id, user_message_id=user_message.id, request_type="library_qa",
        model_name=answer.model_name, input_token_count=None, output_token_count=None, latency_ms=latency, status="completed")
    db.add(request); db.flush()
    ai_message = ConversationMessage(conversation_id=conversation.id, sender_type="ASSISTANT", message_text=answer.text,
        input_method="SYSTEM", message_time=datetime.now(UTC))
    db.add(ai_message); db.flush()
    response = AIResponse(ai_request_id=request.id, ai_message_id=ai_message.id, response_text=answer.text,
        response_summary=answer.text[:500], grounded=answer.grounded, confidence_score=answer.confidence_score)
    db.add(response)
    session = db.get(UserSession, payload.session_id) if payload.session_id else None
    record_event(db, event_type="AI_ANSWERED", session_id=payload.session_id, user_id=conversation.user_id,
        device_id=session.device_id if session else None, input_method="TEXT", content_summary=answer.text[:500])
    db.commit()
    return success_response({"answer": answer.text, "provider": answer.provider, "model_name": answer.model_name,
        "grounded": answer.grounded, "confidence_score": answer.confidence_score, "latency_ms": latency,
        "warning": answer.warning, "next_state": "AI_CHAT"}, "Đã tạo câu trả lời.")


@router.post("/answer/mock")
def mock_answer(payload: AIAnswerRequest) -> dict:
    answer = AIService().answer(payload.question)
    return success_response({"question": payload.question, "answer": answer.text, "request_type": "library_qa",
        "model_name": answer.model_name, "grounded": False, "confidence_score": answer.confidence_score, "latency_ms": 0})
