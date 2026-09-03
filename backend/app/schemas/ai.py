from pydantic import BaseModel, Field
from uuid import UUID


class AIAnswerRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


class AIAnswer(BaseModel):
    answer: str
    request_type: str
    model_name: str
    grounded: bool
    confidence_score: float
    latency_ms: int


class AIRuntimeRequest(BaseModel):
    conversation_id: UUID
    session_id: UUID | None = None
    message_text: str = Field(min_length=1, max_length=4000)
