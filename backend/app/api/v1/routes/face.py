from datetime import UTC, datetime
from decimal import Decimal
from time import perf_counter
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.core.responses import success_response
from app.models.schema import Device, FaceAuthenticationLog, FaceProfile, User, UserSession
from app.services.face_service import FaceProviderUnavailable, FaceService
from app.services.interaction_service import record_event
from app.services.media_storage_service import MediaStorageService, MediaValidationError
from app.services.user_service import calculate_student_year

router = APIRouter()


@router.post("/enroll")
async def enroll(user_id: UUID = Form(), session_id: UUID | None = Form(default=None),
                 device_id: UUID | None = Form(default=None), image_file: UploadFile = File(),
                 db: Session = Depends(get_db)) -> dict:
    user = db.get(User, user_id)
    if user is None: raise AppError(404, "USER_NOT_FOUND", "Không tìm thấy người dùng.")
    storage = MediaStorageService()
    try:
        path = await storage.save_image(image_file, "enrollments")
        result = FaceService().enroll_face(user_id, path)
        profile = db.scalar(select(FaceProfile).where(FaceProfile.user_id == user_id, FaceProfile.active.is_(True), FaceProfile.deleted_at.is_(None)))
        if profile is None:
            profile = FaceProfile(user_id=user_id, enrolled_at=datetime.now(UTC), active=True)
            db.add(profile)
        profile.face_template_ref = result.template_ref; profile.face_template_encrypted = None
        profile.model_name = result.model_name; profile.model_version = "1"; profile.quality_score = Decimal(str(result.quality_score))
        record_event(db, event_type="FACE_ENROLLED", session_id=session_id, user_id=user_id, device_id=device_id)
        db.commit(); db.refresh(profile)
        return success_response({"face_profile_id": str(profile.id), "user_id": str(user_id),
            "provider": "mock", "quality_score": result.quality_score}, "Đăng ký khuôn mặt thành công.")
    except MediaValidationError as exc: raise AppError(400, "INVALID_IMAGE", str(exc)) from exc
    except FaceProviderUnavailable as exc: raise AppError(503, "FACE_PROVIDER_UNAVAILABLE", str(exc)) from exc
    finally:
        if "path" in locals(): storage.cleanup(path)


@router.post("/verify")
async def verify(session_id: UUID | None = Form(default=None), device_code: str | None = Form(default=None),
                 image_file: UploadFile = File(), db: Session = Depends(get_db)) -> dict:
    storage = MediaStorageService(); started = perf_counter()
    session = db.get(UserSession, session_id) if session_id else None
    device = db.scalar(select(Device).where(Device.device_code == device_code)) if device_code else None
    if session_id and session is None: raise AppError(404, "SESSION_NOT_FOUND", "Không tìm thấy phiên kiosk.")
    try:
        path = await storage.save_image(image_file, "verification")
        candidate = db.scalar(select(FaceProfile).where(FaceProfile.active.is_(True), FaceProfile.deleted_at.is_(None)).order_by(FaceProfile.enrolled_at))
        result = FaceService().verify_face(path, candidate.user_id if candidate else None)
        user = db.get(User, result.user_id) if result.user_id else None
        processing_ms = int((perf_counter() - started) * 1000)
        attempt = 1
        if session_id:
            attempt = int(db.scalar(select(func.count(FaceAuthenticationLog.id)).where(FaceAuthenticationLog.session_id == session_id)) or 0) + 1
        log = FaceAuthenticationLog(user_id=result.user_id, session_id=session_id,
            device_id=session.device_id if session else (device.id if device else None), result=result.result,
            confidence_score=Decimal(str(result.confidence_score)), processing_time_ms=processing_ms,
            attempt_number=attempt, failure_reason=None if user else result.result, occurred_at=datetime.now(UTC))
        db.add(log)
        if user and session:
            session.user_id = user.id; session.identified = True
        event_type = "FACE_RECOGNIZED" if user else "FACE_FAILED"
        record_event(db, event_type=event_type, session_id=session_id, user_id=user.id if user else None,
            device_id=log.device_id, success=user is not None)
        db.commit()
        user_data = None if user is None else {"id": str(user.id), "student_code": user.student_code,
            "full_name": user.full_name, "faculty": user.faculty, "major": user.major,
            "admission_year": user.admission_year, "student_year": calculate_student_year(user.admission_year)}
        next_state = "WELCOME" if user else "FACE_UNKNOWN"
        message = f"Xin chào, {user.full_name}!" if user else "Không nhận diện được người dùng."
        return success_response({"result": result.result, "user": user_data, "confidence_score": result.confidence_score,
            "next_state": next_state, "processing_time_ms": processing_ms}, message)
    except MediaValidationError as exc: raise AppError(400, "INVALID_IMAGE", str(exc)) from exc
    except FaceProviderUnavailable as exc: raise AppError(503, "FACE_PROVIDER_UNAVAILABLE", str(exc)) from exc
    finally:
        if "path" in locals(): storage.cleanup(path)
