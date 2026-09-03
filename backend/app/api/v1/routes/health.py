from fastapi import APIRouter
from app.core.config import settings
from app.core.database import check_database_connection
from app.core.errors import AppError
from app.core.responses import success_response
from app.services.media_storage_service import MediaStorageService

router = APIRouter()

@router.get("")
async def detailed_health() -> dict:
    database_status, note = check_database_connection()
    try:
        media_status = "ready" if MediaStorageService().ensure_ready() else "unavailable"
    except OSError:
        media_status = "unavailable"
    return success_response({"app_status": "ok", "database_status": database_status, "database_note": note,
        "environment": settings.environment, "api_version": settings.api_version,
        "providers": {"face_provider": settings.face_provider, "voice_provider": settings.voice_provider,
            "ai_provider": settings.ai_provider}, "media_storage_status": media_status})


@router.get("/db")
async def database_health() -> dict:
    status, note = check_database_connection()
    if status != "connected": raise AppError(503, "DATABASE_UNAVAILABLE", note or "Database connection is unavailable")
    return success_response({"database_status": "connected"}, "PostgreSQL connection is healthy.")
