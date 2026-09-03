from datetime import UTC, datetime
from uuid import uuid4
from fastapi import APIRouter
from app.core.responses import success_response
from app.schemas.session import SessionStartRequest

router = APIRouter()

@router.post("/mock-start")
async def mock_start(payload: SessionStartRequest) -> dict:
    return success_response({"session_id": str(uuid4()), "device_code": payload.device_code, "status": "active",
        "user_id": None, "started_at": datetime.now(UTC).isoformat()}, "Đã bắt đầu phiên kiosk mô phỏng")

@router.get("/{session_id}/mock-summary")
async def mock_summary(session_id: str) -> dict:
    return success_response({"session_id": session_id, "status": "completed", "identified": True,
        "question_count": 3, "started_at": "2026-09-03T08:30:00Z", "ended_at": "2026-09-03T08:37:00Z"})
