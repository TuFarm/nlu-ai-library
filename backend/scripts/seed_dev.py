"""Idempotent development seed. Run from backend: python scripts/seed_dev.py."""
from datetime import UTC, datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.schema import (BookCategory, Device, FaceProfile, KnowledgeChunk,
    KnowledgeDocument, KnowledgeSource, SuggestedBook, Survey, SurveyQuestion, User)


def seed() -> None:
    with SessionLocal() as db:
        device = db.scalar(select(Device).where(Device.device_code == "KIOSK_DEV_01"))
        if not device:
            db.add(Device(device_code="KIOSK_DEV_01", device_name="Kiosk phát triển 01", location="Laptop development", status="active"))

        user = db.scalar(select(User).where(User.student_code == "ITCSIU24092"))
        if not user:
            user = User(student_code="ITCSIU24092", full_name="Phạm Hoàng Tuấn Tú", email="tu.pham@example.edu.vn",
                user_type="student", account_status="active", preferred_language="vi",
                faculty="Khoa Công nghệ Thông tin", major="Công nghệ thông tin", admission_year=2024)
            db.add(user); db.flush()
        profile = db.scalar(select(FaceProfile).where(FaceProfile.user_id == user.id, FaceProfile.active.is_(True)))
        if not profile:
            db.add(FaceProfile(user_id=user.id, face_template_ref=f"mock://seed/{user.id}", model_name="mock-face-v1",
                model_version="1", quality_score=0.95, enrolled_at=datetime.now(UTC), active=True))

        categories = ["Công nghệ thông tin", "Nông nghiệp", "Kinh tế", "Ngoại ngữ", "Kỹ năng mềm"]
        for index, name in enumerate(categories, 1):
            category = db.scalar(select(BookCategory).where(BookCategory.category_name == name))
            if not category:
                category = BookCategory(category_name=name, description=f"Sách gợi ý thuộc chủ đề {name}"); db.add(category); db.flush()
            external_id = f"NLU-SEED-{index:03d}"
            if not db.scalar(select(SuggestedBook).where(SuggestedBook.external_book_id == external_id)):
                db.add(SuggestedBook(category_id=category.id, external_book_id=external_id,
                    title=f"Tài liệu nhập môn {name}", author_name="Thư viện NLU", short_description="Dữ liệu phát triển", source="dev-seed"))

        source = db.scalar(select(KnowledgeSource).where(KnowledgeSource.source_name == "Kiến thức kiosk phát triển"))
        if not source:
            source = KnowledgeSource(source_name="Kiến thức kiosk phát triển", source_type="TEXT",
                original_file_name=None, file_mime_type="text/plain", file_size=None, status="processed")
            db.add(source); db.flush()
        document = db.scalar(select(KnowledgeDocument).where(KnowledgeDocument.source_id == source.id,
            KnowledgeDocument.title == "Thông tin dịch vụ thư viện"))
        if not document:
            document = KnowledgeDocument(source_id=source.id, title="Thông tin dịch vụ thư viện", document_type="FAQ",
                language="vi", version="1", is_active=True, processing_status="processed")
            db.add(document); db.flush()
        chunks = ["Giờ mở cửa thư viện được công bố tại quầy lễ tân và website chính thức.",
            "Thông tin WiFi thư viện được cung cấp tại quầy hỗ trợ.", "Khu vực học nhóm cần được sử dụng đúng nội quy.",
            "Khu vực tự học yên tĩnh yêu cầu người dùng giữ trật tự."]
        for index, text in enumerate(chunks):
            if not db.scalar(select(KnowledgeChunk).where(KnowledgeChunk.document_id == document.id, KnowledgeChunk.chunk_index == index)):
                db.add(KnowledgeChunk(document_id=document.id, chunk_index=index, chunk_text=text, metadata_json={"seed": True}))

        survey = db.scalar(select(Survey).where(Survey.survey_name == "Khảo sát trải nghiệm kiosk", Survey.version == 1))
        if not survey:
            survey = Survey(survey_name="Khảo sát trải nghiệm kiosk", description="Khảo sát phát triển", version=1, active=True)
            db.add(survey); db.flush()
        questions = [(1, "Bạn có hài lòng với câu trả lời của AI không?", "rating"),
            (2, "AI có giúp bạn giảm thời gian hỏi lễ tân không?", "yes_no"),
            (3, "Bạn có muốn sử dụng kiosk này lần sau không?", "yes_no")]
        for order, text, kind in questions:
            if not db.scalar(select(SurveyQuestion).where(SurveyQuestion.survey_id == survey.id, SurveyQuestion.question_order == order)):
                db.add(SurveyQuestion(survey_id=survey.id, question_text=text, question_type=kind, question_order=order))
        db.commit()
    print("Development seed completed without duplicating keyed records.")


if __name__ == "__main__":
    seed()
