from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Library Receptionist Assistant"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://ai_library:ai_library_dev@localhost:5432/ai_library"
    redis_url: str = "redis://localhost:6379/0"
    gemini_api_key: str = ""
    environment: str = "development"
    api_version: str = "v1"
    media_storage_dir: Path = Path(__file__).resolve().parents[2] / "storage" / "media"
    media_retain_development_files: bool = False
    face_provider: str = "mock"
    voice_provider: str = "mock"
    ai_provider: str = "mock"
    kiosk_session_timeout_seconds: int = 60
    face_confidence_threshold: float = 0.75
    max_image_upload_mb: int = 5
    max_audio_upload_mb: int = 15

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
