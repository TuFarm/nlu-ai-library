from uuid import uuid4
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schema import KnowledgeChunk, KnowledgeDocument
from app.core.responses import success_response
from app.schemas.knowledge import KnowledgeSearch, MockKnowledgeUpload

router = APIRouter()
DOCUMENTS = [
    {"id": "doc-01", "title": "Nội quy thư viện", "source_type": "PDF", "status": "processed"},
    {"id": "doc-02", "title": "Giờ mở cửa thư viện", "source_type": "Text", "status": "processed"},
    {"id": "doc-03", "title": "Quy định mượn tài liệu", "source_type": "Word", "status": "processing"},
    {"id": "doc-04", "title": "Hướng dẫn sử dụng phòng học nhóm", "source_type": "PDF", "status": "processed"},
    {"id": "doc-05", "title": "Câu hỏi thường gặp", "source_type": "Web Link", "status": "failed"},
]

@router.get("/sources/mock")
async def sources() -> dict: return success_response([{"id": "src-01", "name": "Kho tài liệu NLU", "document_count": 5, "status": "active"}])

@router.post("/upload/mock")
async def upload(payload: MockKnowledgeUpload) -> dict:
    return success_response({"source_id": str(uuid4()), "file_name": payload.file_name, "source_type": payload.source_type,
        "processing_status": "mock_accepted", "note": "Tệp chưa được lưu hoặc phân tích trong Phase 2."}, "Đã mô phỏng tiếp nhận tài liệu")

@router.get("/documents/mock")
async def documents() -> dict: return success_response(DOCUMENTS)


@router.post("/chunks/search/mock")
def search_chunks(payload: KnowledgeSearch, db: Session = Depends(get_db)) -> dict:
    rows = db.execute(select(KnowledgeChunk, KnowledgeDocument).join(KnowledgeDocument)
        .where(KnowledgeDocument.is_active.is_(True), KnowledgeChunk.chunk_text.ilike(f"%{payload.query}%"))
        .limit(payload.top_k)).all()
    data = [{"chunk_id": str(chunk.id), "document_id": str(document.id), "title": document.title,
        "chunk_text": chunk.chunk_text, "page_number": chunk.page_number} for chunk, document in rows]
    message = "Đã tìm thấy ngữ cảnh phù hợp." if data else "Chưa có đoạn tri thức phù hợp."
    return success_response(data, message)
