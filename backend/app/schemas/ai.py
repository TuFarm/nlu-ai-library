from pydantic import BaseModel, Field


class AIAnswerRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


class AIAnswer(BaseModel):
    answer: str
    request_type: str
    model_name: str
    grounded: bool
    confidence_score: float
    latency_ms: int
