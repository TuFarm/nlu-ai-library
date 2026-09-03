from datetime import UTC, datetime
from uuid import uuid4
from fastapi import APIRouter
from app.core.responses import success_response
from app.schemas.conversation import ConversationStart, MessageCreate

router = APIRouter()

@router.post("/start")
@router.post("/mock-start", include_in_schema=False)
async def start(_: ConversationStart) -> dict: return success_response({"conversation_id": str(uuid4()), "status": "active"})

@router.post("/{conversation_id}/messages")
@router.post("/{conversation_id}/messages/mock", include_in_schema=False)
async def save_message(conversation_id: str, payload: MessageCreate) -> dict:
    return success_response({"id": str(uuid4()), "conversation_id": conversation_id, "role": "user", "text": payload.text, "created_at": datetime.now(UTC).isoformat()})

@router.get("/{conversation_id}/messages/mock")
async def history(conversation_id: str) -> dict:
    return success_response([{"id": "msg-01", "conversation_id": conversation_id, "role": "user", "text": "Thư viện mở cửa lúc mấy giờ?"}, {"id": "msg-02", "conversation_id": conversation_id, "role": "assistant", "text": "Đây là câu trả lời mô phỏng từ nguồn tri thức thư viện."}])
