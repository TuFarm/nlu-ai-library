import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Iterable
from uuid import UUID

from app.core.config import settings
from app.utils.image_utils import filename_requests_unknown


class FaceProviderUnavailable(RuntimeError):
    pass


class FaceImageError(ValueError):
    pass


@dataclass
class FaceEnrollmentResult:
    template_ref: str | None
    template_bytes: bytes | None
    model_name: str
    quality_score: float


@dataclass
class FaceVerificationResult:
    result: str
    user_id: UUID | None
    confidence_score: float | None


FaceCandidate = tuple[UUID, bytes | None, str | None]


def _load_local_library():
    try:
        import face_recognition  # type: ignore[import-not-found]
    except (ImportError, SystemExit) as exc:
        raise FaceProviderUnavailable(
            "FaceID cục bộ chưa sẵn sàng. Hãy cài lại requirements-face-local.txt "
            "(bao gồm setuptools<82 cho face_recognition_models) hoặc chuyển "
            "FACE_PROVIDER=mock."
        ) from exc
    return face_recognition


def _extract_single_encoding(image_path: Path):
    face_recognition = _load_local_library()
    image = face_recognition.load_image_file(str(image_path))
    locations = face_recognition.face_locations(image, model="hog")
    if not locations:
        raise FaceImageError("Không phát hiện khuôn mặt trong ảnh. Vui lòng nhìn thẳng vào camera.")
    if len(locations) != 1:
        raise FaceImageError("Ảnh đăng ký phải có đúng một khuôn mặt.")
    encodings = face_recognition.face_encodings(image, known_face_locations=locations)
    if len(encodings) != 1:
        raise FaceImageError("Không thể trích xuất đặc trưng khuôn mặt từ ảnh.")
    return encodings[0]


class FaceService:
    def enroll_face(self, user_id: UUID, image_path: Path) -> FaceEnrollmentResult:
        if settings.face_provider == "local":
            encoding = _extract_single_encoding(image_path)
            serialized = json.dumps([float(value) for value in encoding]).encode("utf-8")
            return FaceEnrollmentResult(None, serialized, "face-recognition-hog-128d", 1.0)
        digest = sha256(image_path.read_bytes()).hexdigest()
        return FaceEnrollmentResult(f"mock://face/{user_id}/{digest}", None, "mock-face-v1", 0.95)

    def verify_face(self, image_path: Path, candidates: Iterable[FaceCandidate] | UUID | None) -> FaceVerificationResult:
        # UUID/None compatibility keeps the Phase 3 service boundary usable.
        if isinstance(candidates, UUID):
            candidate_list: list[FaceCandidate] = [(candidates, None, None)]
        elif candidates is None:
            candidate_list = []
        else:
            candidate_list = list(candidates)
        if settings.face_provider == "local":
            face_recognition = _load_local_library()
            probe = _extract_single_encoding(image_path)
            valid_users: list[UUID] = []
            known_encodings = []
            for user_id, template_bytes, _template_ref in candidate_list:
                if not template_bytes:
                    continue
                try:
                    values = json.loads(template_bytes.decode("utf-8"))
                    if isinstance(values, list) and len(values) == 128:
                        known_encodings.append(values)
                        valid_users.append(user_id)
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
            if not known_encodings:
                return FaceVerificationResult("UNKNOWN_FACE", None, None)
            distances = face_recognition.face_distance(known_encodings, probe)
            best_index = min(range(len(distances)), key=lambda index: float(distances[index]))
            confidence = round(max(0.0, min(1.0, 1.0 - float(distances[best_index]))), 4)
            if confidence >= settings.face_confidence_threshold:
                return FaceVerificationResult("SUCCESS", valid_users[best_index], confidence)
            result = "LOW_CONFIDENCE" if confidence >= max(0.0, settings.face_confidence_threshold - 0.15) else "UNKNOWN_FACE"
            return FaceVerificationResult(result, None, confidence)

        candidate_user_id = candidate_list[0][0] if candidate_list else None
        if "low" in image_path.name.lower():
            return FaceVerificationResult("LOW_CONFIDENCE", None, min(0.60, settings.face_confidence_threshold - 0.01))
        if filename_requests_unknown(image_path) or candidate_user_id is None:
            return FaceVerificationResult("UNKNOWN_FACE", None, 0.31)
        confidence = 0.94
        if confidence < settings.face_confidence_threshold:
            return FaceVerificationResult("LOW_CONFIDENCE", None, confidence)
        return FaceVerificationResult("SUCCESS", candidate_user_id, confidence)
