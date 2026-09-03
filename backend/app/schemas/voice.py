from uuid import UUID

from pydantic import BaseModel, Field


class BrowserTranscriptCreate(BaseModel):
    session_id: UUID | None = None
    conversation_id: UUID
    transcript: str = Field(min_length=1, max_length=4000)
    confidence_score: float | None = Field(default=None, ge=0, le=1)
