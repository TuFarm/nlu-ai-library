from dataclasses import dataclass

import httpx

from app.core.config import settings


SYSTEM_INSTRUCTION = """Bạn là Trợ lý AI Lễ tân Thư viện Đại học Nông Lâm.
Luôn trả lời bằng tiếng Việt, thân thiện, ngắn gọn và phù hợp để đọc thành tiếng tại kiosk.
Bạn có thể hỗ trợ các câu hỏi chung về việc sử dụng thư viện. RAG và tài liệu nội bộ chưa được kết nối.
Không được bịa giờ mở cửa, chính sách, mật khẩu WiFi, vị trí hoặc thông tin chính thức.
Khi thiếu tài liệu chính thức, hãy nói đúng câu:
"Hiện tại tôi chưa được cung cấp tài liệu chính thức về nội dung này. Bạn vui lòng liên hệ quầy lễ tân hoặc tải tài liệu vào hệ thống để tôi trả lời chính xác hơn."
Không tuyên bố rằng bạn là nhân viên con người."""


@dataclass
class AnswerResult:
    text: str
    provider: str
    model_name: str
    grounded: bool = False
    confidence_score: float = 0.72
    warning: str | None = None
    used_fallback: bool = False
    provider_error: bool = False


def _mock_answer(question: str, warning: str | None = None, provider_error: bool = False) -> AnswerResult:
    normalized = question.casefold()
    unavailable = ("Hiện tại tôi chưa được cung cấp tài liệu chính thức về nội dung này. "
        "Bạn vui lòng liên hệ quầy lễ tân hoặc tải tài liệu vào hệ thống để tôi trả lời chính xác hơn.")
    if "học nhóm" in normalized:
        text = "Thư viện có khu vực học nhóm, nhưng tôi chưa có tài liệu chính thức về vị trí phòng. " + unavailable
    elif "wifi" in normalized:
        text = "Tôi chưa có tài liệu chính thức về WiFi thư viện. " + unavailable
    elif any(term in normalized for term in ("mở cửa", "giờ", "chính sách")):
        text = unavailable
    else:
        text = "Tôi đã ghi nhận câu hỏi của bạn. " + unavailable
    return AnswerResult(text, "mock", "mock-model", warning=warning,
        used_fallback=warning is not None, provider_error=provider_error)


class AIService:
    def answer(self, question: str, history: list[dict[str, str]] | None = None) -> AnswerResult:
        if settings.ai_provider != "gemini":
            return _mock_answer(question)
        if not settings.gemini_api_key:
            return _mock_answer(question, "GEMINI_API_KEY is missing; using mock answer.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent"
        contents = [{"role": item["role"], "parts": [{"text": item["text"]}]} for item in (history or [])]
        contents.append({"role": "user", "parts": [{"text": question}]})
        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
            "contents": contents,
        }
        try:
            response = httpx.post(
                url,
                headers={"x-goog-api-key": settings.gemini_api_key, "Content-Type": "application/json"},
                json=payload,
                timeout=settings.gemini_timeout_seconds,
            )
            response.raise_for_status()
            body = response.json()
            parts = body.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            text = "".join(part.get("text", "") for part in parts).strip()
            if not text:
                raise ValueError("Gemini response contained no text.")
            return AnswerResult(text, "gemini", settings.gemini_model, confidence_score=0.8)
        except (httpx.HTTPError, ValueError, KeyError, IndexError) as exc:
            return _mock_answer(question, f"Gemini unavailable; using mock answer ({type(exc).__name__}).", provider_error=True)
