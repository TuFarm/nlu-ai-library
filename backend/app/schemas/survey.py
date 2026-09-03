from typing import Any

from pydantic import BaseModel, Field


class SurveySubmission(BaseModel):
    answers: dict[str, Any] = Field(min_length=1)
