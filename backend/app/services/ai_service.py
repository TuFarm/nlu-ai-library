from dataclasses import dataclass

from app.core.config import settings


@dataclass
class AnswerResult:
    text: str
    provider: str
    model_name: str
    grounded: bool = False
    confidence_score: float = 0.72
    warning: str | None = None


class AIService:
    def answer(self, question: str) -> AnswerResult:
        normalized = question.casefold()
        if "wifi" in normalized:
            text = "Ở bản thử nghiệm, tôi chưa kết nối kho tài liệu thật. Sau khi tích hợp RAG, tôi sẽ tra cứu tài liệu nội bộ để trả lời chính xác thông tin WiFi của thư viện."
        elif "mở cửa" in normalized or "giờ" in normalized:
            text = "Thư viện mở cửa theo lịch trong tài liệu nội bộ. Hiện câu trả lời này đang ở chế độ mô phỏng; RAG sẽ cung cấp giờ chính xác ở bước tiếp theo."
        elif "học nhóm" in normalized:
            text = "Thư viện có khu vực học nhóm. Bản thử nghiệm chưa truy xuất được vị trí phòng cụ thể từ kho tri thức."
        else:
            text = "Tôi đã ghi nhận câu hỏi của bạn. Hiện hệ thống dùng câu trả lời mô phỏng và sẽ bổ sung ngữ cảnh chính xác khi Gemini/RAG được tích hợp."
        warning = None
        if settings.ai_provider == "gemini": warning = "Gemini integration is pending; using mock answer." if settings.gemini_api_key else "GEMINI_API_KEY is missing; using mock answer."
        return AnswerResult(text, "mock", "mock-model", warning=warning)
