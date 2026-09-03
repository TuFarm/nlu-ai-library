from fastapi.testclient import TestClient

from app.main import app
from app.services.user_service import calculate_student_year

client = TestClient(app)


def test_health_endpoints():
    assert client.get("/health").json()["data"]["status"] == "ok"
    detail = client.get("/api/v1/health").json()["data"]
    assert detail["app_status"] == "ok"
    assert detail["database_status"] in {"connected", "unavailable"}
    assert "database_url" not in detail


def test_mock_user_and_student_year():
    user = client.get("/api/v1/users/me/mock").json()["data"]
    assert user["student_code"] == "ITCSIU24092"
    assert user["calculated_student_year"] == calculate_student_year(2024)
    assert calculate_student_year(None, 2026) is None
    assert calculate_student_year(2027, 2026) is None


def test_mock_face_success_and_unknown_identity():
    success = client.post("/api/v1/face/verify/mock", json={"scenario": "SUCCESS"}).json()["data"]
    unknown = client.post("/api/v1/face/verify/mock", json={"scenario": "UNKNOWN_FACE"}).json()["data"]
    assert success["user"]["student_code"] == "ITCSIU24092"
    assert unknown["user"] is None
    assert success["next_state"] == "WELCOME"
    assert unknown["next_state"] == "FACE_UNKNOWN"


def test_kiosk_session_flow():
    started = client.post("/api/v1/kiosk/sessions/start").json()["data"]
    assert started["status"] == "active"
    assert started["next_state"] == "FACE_SCANNING"
    ended = client.post(f"/api/v1/kiosk/sessions/{started['session_id']}/end").json()["data"]
    assert ended["next_state"] == "IDLE"


def test_mock_report_overview():
    data = client.get("/api/v1/reports/overview/mock").json()["data"]
    assert data["total_sessions"] > 0
    assert data["avg_satisfaction_score"] <= 5
