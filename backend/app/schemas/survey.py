from typing import Any

from pydantic import BaseModel, Field
from uuid import UUID


class SurveySubmission(BaseModel):
    answers: dict[str, Any] = Field(min_length=1)
    session_id: UUID | None = None
    user_id: UUID | None = None
