from pydantic import BaseModel


class ReportOverview(BaseModel):
    total_sessions: int
    total_identified_users: int
    total_questions: int
    total_ai_answers: int
    total_surveys: int
    avg_satisfaction_score: float
    avg_ai_response_time_ms: float
