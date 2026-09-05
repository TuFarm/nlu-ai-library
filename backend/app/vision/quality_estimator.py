from dataclasses import dataclass
from typing import Any

from app.vision.face_detector import DetectedFace
from app.vision.face_tracker import Track


@dataclass(frozen=True)
class QualityResult:
    accepted: bool
    guidance: str | None
    score: float


class QualityEstimator:
    def estimate(self, image: Any, face: DetectedFace, track: Track, face_count: int, now: float) -> QualityResult:
        import numpy as np
        top, right, bottom, left = face.box
        crop = image[top:bottom, left:right].mean(axis=2)
        if face_count != 1:
            return QualityResult(False, "Vui lòng đứng một mình trước kiosk", 0)
        if min(bottom - top, right - left) < 160:
            return QualityResult(False, "Vui lòng đến gần hơn", .2)
        brightness = float(crop.mean())
        if brightness < 55:
            return QualityResult(False, "Khuôn mặt đang thiếu sáng", .3)
        if brightness > 205:
            return QualityResult(False, "Ánh sáng phía sau quá mạnh", .3)
        laplacian = -4 * crop[1:-1, 1:-1] + crop[:-2, 1:-1] + crop[2:, 1:-1] + crop[1:-1, :-2] + crop[1:-1, 2:]
        if float(np.var(laplacian)) < 75:
            return QualityResult(False, "Giữ yên khuôn mặt", .4)
        marks = face.landmarks
        eyes = [np.asarray(marks[name]) for name in ("left_eye", "right_eye")]
        eyes_open = all(np.linalg.norm(eye[1] - eye[5]) / max(1, np.linalg.norm(eye[0] - eye[3])) > .14 for eye in eyes)
        centers = [eye.mean(axis=0) for eye in eyes]
        eye_span = max(1, np.linalg.norm(centers[0] - centers[1]))
        nose = np.asarray(marks["nose_tip"]).mean(axis=0)
        midpoint = (centers[0] + centers[1]) / 2
        frontal = abs(nose[0] - midpoint[0]) / eye_span < .28 and abs(centers[0][1] - centers[1][1]) / eye_span < .16
        if not eyes_open or not frontal:
            return QualityResult(False, "Vui lòng nhìn thẳng vào camera", .5)
        if now - track.stable_since < .8:
            return QualityResult(False, "Giữ yên trong giây lát", .7)
        return QualityResult(True, None, 1.0)
