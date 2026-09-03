from fastapi import APIRouter
from app.core.responses import success_response
from app.schemas.survey import SurveySubmission

router = APIRouter()

@router.get("/active/mock")
async def active() -> dict:
    texts = [("q1", "Bạn có hài lòng với câu trả lời của AI không?", "rating"), ("q2", "AI có giúp bạn giảm thời gian hỏi lễ tân không?", "yes_no"), ("q3", "Bạn có muốn sử dụng kiosk này lần sau không?", "yes_no"), ("q4", "Bạn đánh giá tốc độ phản hồi của AI như thế nào?", "rating")]
    return success_response({"id": "survey-2026-01", "name": "Khảo sát trải nghiệm kiosk", "questions": [{"id": i, "text": t, "type": k} for i, t, k in texts]})

@router.post("/{survey_id}/responses/mock")
async def submit(survey_id: str, payload: SurveySubmission) -> dict:
    return success_response({"survey_id": survey_id, "answer_count": len(payload.answers), "stored": False}, "Cảm ơn bạn đã gửi phản hồi!")
