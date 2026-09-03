from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.core.responses import success_response
from app.models.schema import UserSession
from app.schemas.kiosk import KioskEventCreate, KioskSessionEnd, KioskSessionStart
from app.services.interaction_service import record_event
from app.services.kiosk_service import end_session, start_session

router = APIRouter()


@router.post("/sessions/start")
def start(payload: KioskSessionStart, db: Session = Depends(get_db)) -> dict:
    session, device = start_session(db, payload.device_code)
    return success_response({"session_id": str(session.id), "device_id": str(device.id), "status": "active",
        "next_state": "FACE_SCANNING"}, "Đã bắt đầu phiên kiosk")


@router.post("/sessions/{session_id}/end")
def end(session_id: UUID, payload: KioskSessionEnd, db: Session = Depends(get_db)) -> dict:
    session = end_session(db, session_id, payload.exit_reason)
    if session is None: raise AppError(404, "SESSION_NOT_FOUND", "Không tìm thấy phiên kiosk.")
    return success_response({"session_id": str(session.id), "duration_seconds": session.duration_seconds, "next_state": "IDLE"}, "Đã kết thúc phiên kiosk")


@router.post("/sessions/{session_id}/events")
def create_event(session_id: UUID, payload: KioskEventCreate, db: Session = Depends(get_db)) -> dict:
    session = db.get(UserSession, session_id)
    if session is None: raise AppError(404, "SESSION_NOT_FOUND", "Không tìm thấy phiên kiosk.")
    event = record_event(db, session_id=session.id, user_id=session.user_id, device_id=session.device_id,
        event_type=payload.event_type, input_method=payload.input_method,
        content_summary=payload.content_summary, success=payload.success)
    db.commit()
    return success_response({"event_id": str(event.id), "event_type": event.event_type, "event_time": event.event_time.isoformat()})
