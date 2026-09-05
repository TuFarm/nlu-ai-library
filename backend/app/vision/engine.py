from io import BytesIO
from time import monotonic

from app.vision.face_detector import FaceDetector
from app.vision.face_tracker import FaceTracker
from app.vision.quality_estimator import QualityEstimator


class VisionEngine:
    def __init__(self, detector=None, tracker=None, quality=None):
        self.detector = detector or FaceDetector()
        self.tracker = tracker or FaceTracker()
        self.quality = quality or QualityEstimator()

    @property
    def tracks(self):
        return self.tracker.tracks

    def inspect(self, data):
        import numpy as np
        from PIL import Image
        with Image.open(BytesIO(data)) as source:
            if source.width > 1920 or source.height > 1080:
                raise ValueError("Frame dimensions exceed 1920×1080")
            image = np.asarray(source.convert("RGB"))
        faces = self.detector.detect(image)
        now = monotonic()
        tracks = self.tracker.update([face.box for face in faces], now)
        results = []
        for face, track in zip(faces, tracks, strict=True):
            quality = self.quality.estimate(image, face, track, len(tracks), now)
            if not quality.accepted:
                track.reset()
            landmarks = [[int(x), int(y)] for points in face.landmarks.values() for x, y in points]
            results.append({
                "track_id": track.id,
                "box": list(track.box),
                "landmarks": landmarks,
                "quality_ok": quality.accepted,
                "quality_score": quality.score,
                "guidance": quality.guidance,
            })
        return image, results
