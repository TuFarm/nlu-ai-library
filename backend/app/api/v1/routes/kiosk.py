from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter

from app.core.responses import success_response

router = APIRouter()


@router.post("/sessions/start")
async def start_kiosk_session() -> dict:
    return success_response({"session_id": str(uuid4()), "status": "active", "user_id": None,
        "started_at": datetime.now(UTC).isoformat(), "next_state": "FACE_SCANNING"}, "Đã bắt đầu phiên kiosk")


@router.post("/sessions/{session_id}/end")
async def end_kiosk_session(session_id: str) -> dict:
    return success_response({"session_id": session_id, "status": "completed",
        "ended_at": datetime.now(UTC).isoformat(), "next_state": "IDLE"}, "Đã kết thúc phiên kiosk")
