from fastapi import APIRouter
from app.core.responses import success_response
from app.schemas.face import FaceVerifyRequest

router = APIRouter()

@router.post("/verify/mock")
async def mock_verify(payload: FaceVerifyRequest) -> dict:
    results = {
        "SUCCESS": {"result": "SUCCESS", "user": {"id": "d8f8b7db-56b5-4be5-a136-19eb154ae21f", "full_name": "Phạm Hoàng Tuấn Tú", "student_code": "ITCSIU24092", "faculty": "Khoa Công nghệ Thông tin", "major": "Công nghệ thông tin", "admission_year": 2024, "student_year": 3}, "confidence_score": 0.94, "next_state": "WELCOME", "message": "Xin chào, Phạm Hoàng Tuấn Tú!"},
        "UNKNOWN_FACE": {"result": "UNKNOWN_FACE", "user": None, "confidence_score": 0.31, "next_state": "FACE_UNKNOWN", "message": "Không nhận diện được người dùng."},
        "LOW_CONFIDENCE": {"result": "LOW_CONFIDENCE", "user": None, "confidence_score": 0.48, "next_state": "FACE_UNKNOWN", "message": "Độ tin cậy thấp. Vui lòng thử lại."},
        "TIMEOUT": {"result": "TIMEOUT", "user": None, "confidence_score": 0.0, "next_state": "FACE_UNKNOWN", "message": "Quá thời gian nhận diện. Vui lòng thử lại."},
        "ERROR": {"result": "ERROR", "user": None, "confidence_score": 0.0, "next_state": "ERROR", "message": "Có lỗi khi nhận diện khuôn mặt."},
        "FAILED": {"result": "FAILED", "user": None, "confidence_score": 0.0, "next_state": "ERROR", "message": "Nhận diện thất bại."},
    }
    return success_response(results[payload.scenario])
