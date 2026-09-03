from pathlib import Path
from uuid import UUID

from app.services.ai_service import AIService
from app.services.face_service import FaceService
from app.services.user_service import calculate_student_year
from fastapi.testclient import TestClient
from types import SimpleNamespace
from app.main import app
from app.core.database import get_db


def test_face_mock_is_deterministic_and_supports_unknown(tmp_path: Path):
    user_id = UUID("11111111-1111-1111-1111-111111111111")
    image = tmp_path / "known.jpg"; image.write_bytes(b"test-image")
    first = FaceService().enroll_face(user_id, image)
    second = FaceService().enroll_face(user_id, image)
    assert first.template_ref == second.template_ref
    assert FaceService().verify_face(image, user_id).result == "SUCCESS"
    unknown = tmp_path / "unknown-face.jpg"; unknown.write_bytes(b"test-image-2")
    result = FaceService().verify_face(unknown, user_id)
    assert result.result == "UNKNOWN_FACE" and result.user_id is None


def test_contextual_mock_ai_and_student_year():
    assert "WiFi" in AIService().answer("Wifi thư viện là gì?").text
    assert calculate_student_year(2024, 2026) == 3


def test_browser_transcript_endpoint_persists_message_contract(monkeypatch):
    from app.api.v1.routes import voice
    conversation_id = UUID("33333333-3333-3333-3333-333333333333")
    message_id = UUID("44444444-4444-4444-4444-444444444444")
    fake_conversation = SimpleNamespace(id=conversation_id, session_id=UUID("55555555-5555-5555-5555-555555555555"), user_id=None)
    class FakeDB:
        def get(self, model, identifier): return fake_conversation
    app.dependency_overrides[get_db] = lambda: FakeDB()
    monkeypatch.setattr(voice, "save_message", lambda *args: SimpleNamespace(id=message_id))
    try:
        response = TestClient(app).post("/api/v1/voice/browser-transcript", json={
            "conversation_id": str(conversation_id), "transcript": "Thư viện mở cửa lúc mấy giờ?", "confidence_score": 0.91})
        assert response.status_code == 200
        assert response.json()["data"]["message_id"] == str(message_id)
    finally:
        app.dependency_overrides.clear()
