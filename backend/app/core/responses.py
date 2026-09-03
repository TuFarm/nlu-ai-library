from typing import Any

from pydantic import BaseModel


class ApiError(BaseModel):
    code: str
    details: Any = None


class ApiResponse(BaseModel):
    success: bool = True
    message: str = "OK"
    data: Any = None
    error: ApiError | None = None


def success_response(data: Any = None, message: str = "OK") -> dict[str, Any]:
    return {"success": True, "message": message, "data": data}
