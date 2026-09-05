from dataclasses import dataclass
from typing import Any

from app.services.face_service import _load_local_library


@dataclass(frozen=True)
class DetectedFace:
    box: tuple[int, int, int, int]
    landmarks: dict[str, list[tuple[int, int]]]


class FaceDetector:
    """Runs detection for every accepted frame; recognition has its own slower cadence."""

    def detect(self, image: Any) -> list[DetectedFace]:
        library = _load_local_library()
        boxes = library.face_locations(image, model="hog")
        landmarks = library.face_landmarks(image, boxes)
        return [DetectedFace(tuple(box), marks) for box, marks in zip(boxes, landmarks, strict=True)]
