from fastapi import APIRouter

from app.core.responses import success_response

router = APIRouter()


@router.get("/dashboard/mock")
async def dashboard() -> dict:
    return success_response({"total_sessions": 1284, "identified_users": 947, "questions": 3260,
        "ai_answers": 3198, "surveys": 486, "avg_satisfaction": 4.6})


@router.get("/status")
async def status() -> dict:
    return success_response([{"module": "Database", "status": "Completed"},
        {"module": "Kiosk flow", "status": "Mock only"}, {"module": "FaceID", "status": "Mock only"},
        {"module": "Gemini/RAG", "status": "Not implemented"}])
