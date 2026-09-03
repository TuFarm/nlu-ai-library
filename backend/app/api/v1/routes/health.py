from fastapi import APIRouter
from app.core.config import settings
from app.core.database import check_database_connection
from app.core.responses import success_response

router = APIRouter()

@router.get("")
async def detailed_health() -> dict:
    database_status, note = check_database_connection()
    return success_response({"app_status": "ok", "database_status": database_status, "database_note": note,
        "environment": settings.environment, "api_version": settings.api_version})
