from __future__ import annotations

import hashlib
import re
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.utils.audio_utils import has_supported_audio_signature
from app.utils.image_utils import has_supported_image_signature


class MediaValidationError(ValueError):
    pass


class MediaStorageService:
    IMAGE_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
    AUDIO_TYPES = {"audio/wav": ".wav", "audio/x-wav": ".wav", "audio/webm": ".webm", "audio/mpeg": ".mp3", "audio/mp4": ".m4a", "audio/ogg": ".ogg"}

    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root or settings.media_storage_dir).resolve()

    def ensure_ready(self) -> bool:
        for relative in ("faces/enrollments", "faces/verification", "audio/recordings"):
            (self.root / relative).mkdir(parents=True, exist_ok=True)
        return self.root.is_dir()

    async def save_image(self, upload: UploadFile, purpose: str) -> Path:
        return await self._save(upload, f"faces/{purpose}", self.IMAGE_TYPES, settings.max_image_upload_mb)

    async def save_audio(self, upload: UploadFile) -> Path:
        return await self._save(upload, "audio/recordings", self.AUDIO_TYPES, settings.max_audio_upload_mb)

    async def _save(self, upload: UploadFile, relative: str, allowed: dict[str, str], max_mb: int) -> Path:
        content_type = (upload.content_type or "").lower()
        if content_type not in allowed:
            raise MediaValidationError(f"Unsupported media type: {content_type or 'unknown'}")
        content = await upload.read(max_mb * 1024 * 1024 + 1)
        if not content or len(content) > max_mb * 1024 * 1024:
            raise MediaValidationError(f"Media must be between 1 byte and {max_mb} MB")
        signature_valid = (has_supported_image_signature(content, content_type) if content_type.startswith("image/")
            else has_supported_audio_signature(content, content_type))
        if not signature_valid:
            raise MediaValidationError("Media content does not match its declared type")
        # UUID names prevent traversal/collisions; original name only contributes a safe test hint.
        hint = re.sub(r"[^a-z0-9_-]", "", Path(upload.filename or "media").stem.lower())[:30]
        digest = hashlib.sha256(content).hexdigest()[:12]
        target_dir = self.root / relative
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{uuid4().hex}_{hint}_{digest}{allowed[content_type]}"
        target.write_bytes(content)
        return target

    def cleanup(self, path: Path) -> None:
        if not settings.media_retain_development_files and path.is_file() and self.root in path.resolve().parents:
            path.unlink()
