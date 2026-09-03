from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.schema import InteractionEvent


def record_event(db: Session, *, event_type: str, session_id: UUID | None = None,
                 user_id: UUID | None = None, device_id: UUID | None = None,
                 input_method: str | None = None, content_summary: str | None = None,
                 success: bool | None = True) -> InteractionEvent:
    event = InteractionEvent(session_id=session_id, user_id=user_id, device_id=device_id,
        event_type=event_type, event_time=datetime.now(UTC), input_method=input_method,
        content_summary=content_summary, success=success)
    db.add(event)
    db.flush()
    return event
