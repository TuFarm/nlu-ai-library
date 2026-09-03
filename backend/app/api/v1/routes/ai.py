from fastapi import APIRouter
from app.core.responses import success_response
from app.schemas.ai import AIAnswerRequest

router = APIRouter()

@router.post("/answer/mock")
async def answer(payload: AIAnswerRequest) -> dict:
    return success_response({"question": payload.question, "answer": "Thư viện thường mở cửa theo khung giờ được quy định trong tài liệu nội bộ. Ở bản thử nghiệm này, câu trả lời đang được mô phỏng. Khi tích hợp RAG, hệ thống sẽ truy xuất tài liệu đã tải lên để trả lời chính xác hơn.", "request_type": "library_qa", "model_name": "mock-model", "grounded": False, "confidence_score": 0.72, "latency_ms": 180})
