from typing import Literal

from pydantic import BaseModel, Field


class FaceVerifyRequest(BaseModel):
    scenario: Literal["SUCCESS", "UNKNOWN_FACE", "LOW_CONFIDENCE", "TIMEOUT", "ERROR", "FAILED"] = "SUCCESS"


class FaceUser(BaseModel):
    id: str | None = None
    full_name: str
    student_code: str


class FaceVerifyResult(BaseModel):
    result: str
    user: FaceUser | None
    confidence_score: float = Field(ge=0, le=1)
    message: str
