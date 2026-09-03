from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from uuid import UUID

from app.core.config import settings
from app.utils.image_utils import filename_requests_unknown


class FaceProviderUnavailable(RuntimeError):
    pass


@dataclass
class FaceEnrollmentResult:
    template_ref: str
    model_name: str
    quality_score: float


@dataclass
class FaceVerificationResult:
    result: str
    user_id: UUID | None
    confidence_score: float


class FaceService:
    def enroll_face(self, user_id: UUID, image_path: Path) -> FaceEnrollmentResult:
        if settings.face_provider == "local":
            raise FaceProviderUnavailable("Local face recognition provider is not installed or configured.")
        digest = sha256(image_path.read_bytes()).hexdigest()
        return FaceEnrollmentResult(f"mock://face/{user_id}/{digest}", "mock-face-v1", 0.95)

    def verify_face(self, image_path: Path, candidate_user_id: UUID | None) -> FaceVerificationResult:
        if settings.face_provider == "local":
            raise FaceProviderUnavailable("Local face recognition provider is not installed or configured.")
        if "low" in image_path.name.lower():
            return FaceVerificationResult("LOW_CONFIDENCE", None, min(0.60, settings.face_confidence_threshold - 0.01))
        if filename_requests_unknown(image_path) or candidate_user_id is None:
            return FaceVerificationResult("UNKNOWN_FACE", None, 0.31)
        confidence = 0.94
        if confidence < settings.face_confidence_threshold:
            return FaceVerificationResult("LOW_CONFIDENCE", None, confidence)
        return FaceVerificationResult("SUCCESS", candidate_user_id, confidence)
