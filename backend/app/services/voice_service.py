from dataclasses import dataclass
from pathlib import Path

from app.core.config import settings


@dataclass
class TranscriptionResult:
    transcript: str
    provider: str
    confidence_score: float | None = None
    warning: str | None = None


class VoiceService:
    def transcribe(self, _: Path) -> TranscriptionResult:
        if settings.voice_provider == "browser":
            return TranscriptionResult("", "browser", warning="Use /voice/browser-transcript with Web Speech API output.")
        if settings.voice_provider == "gemini":
            warning = "Gemini STT integration is pending; mock transcript returned."
            if not settings.gemini_api_key: warning = "GEMINI_API_KEY is missing; mock transcript returned."
            return TranscriptionResult("Thư viện mở cửa lúc mấy giờ?", "mock", warning=warning)
        return TranscriptionResult("Thư viện mở cửa lúc mấy giờ?", "mock")
