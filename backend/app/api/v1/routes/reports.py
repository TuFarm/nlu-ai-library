from fastapi import APIRouter
from app.schemas import ModuleStatus
router = APIRouter()
@router.get("/status", response_model=ModuleStatus)
async def status() -> ModuleStatus: return ModuleStatus(module="reports")
