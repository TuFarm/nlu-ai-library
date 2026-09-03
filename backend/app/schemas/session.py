from pydantic import BaseModel


class SessionStartRequest(BaseModel):
    device_code: str = "KIOSK-NLU-01"


class SessionSummary(BaseModel):
    session_id: str
    status: str
    identified: bool
    question_count: int
    started_at: str
    ended_at: str | None = None
