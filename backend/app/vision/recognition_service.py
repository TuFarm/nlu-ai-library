from app.services.face_service import FaceProviderUnavailable, FaceService


class RecognitionService:
    cadence_seconds = .5

    def should_recognize(self, track, now: float) -> bool:
        return now - track.last_recognition >= self.cadence_seconds

    def recognize(self, image_path, candidates):
        return FaceService().verify_face(image_path, candidates)


__all__ = ["RecognitionService", "FaceProviderUnavailable"]
