from fastapi import APIRouter
from app.core.responses import success_response

router = APIRouter()

@router.get("/overview/mock")
async def overview() -> dict:
    return success_response({"total_sessions": 1284, "total_identified_users": 947, "total_questions": 3260, "total_ai_answers": 3198, "total_surveys": 486, "avg_satisfaction_score": 4.6, "avg_ai_response_time_ms": 842.5})

@router.get("/feature-status")
async def feature_status() -> dict:
    modules = [("Database", "Completed"), ("Backend Foundation", "In Progress"), ("Frontend Foundation", "In Progress"), ("FaceID", "Mock only"), ("AI Chat", "Mock only"), ("Knowledge Upload", "Placeholder"), ("RAG", "Not implemented"), ("Dashboard", "Basic placeholder")]
    return success_response([{"module": module, "status": status} for module, status in modules])
