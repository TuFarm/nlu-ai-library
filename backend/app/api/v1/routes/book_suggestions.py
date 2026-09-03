from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.responses import success_response
from app.core.database import get_db
from app.models.schema import BookCategory, SuggestedBook

router = APIRouter()
CATEGORIES = ["Công nghệ thông tin", "Nông nghiệp", "Kinh tế", "Ngoại ngữ", "Kỹ năng mềm"]
BOOKS = [
    {"external_book_id": "NLU-IT-001", "title": "Nhập môn trí tuệ nhân tạo", "author_name": "Nguyễn Văn A", "category": "Công nghệ thông tin"},
    {"external_book_id": "NLU-AG-014", "title": "Nông nghiệp thông minh", "author_name": "Trần Thị B", "category": "Nông nghiệp"},
    {"external_book_id": "NLU-EC-009", "title": "Kinh tế học căn bản", "author_name": "Lê Văn C", "category": "Kinh tế"},
    {"external_book_id": "NLU-LA-021", "title": "English for University", "author_name": "Jane Smith", "category": "Ngoại ngữ"},
    {"external_book_id": "NLU-SK-003", "title": "Kỹ năng học đại học", "author_name": "Phạm Minh D", "category": "Kỹ năng mềm"},
]

@router.get("/book-categories/mock")
async def categories() -> dict: return success_response(CATEGORIES)

@router.get("/suggested-books/mock")
async def books(category: str | None = Query(default=None)) -> dict:
    return success_response([book for book in BOOKS if category is None or book["category"] == category])


@router.get("/book-categories")
def database_categories(db: Session = Depends(get_db)) -> dict:
    rows = db.scalars(select(BookCategory).where(BookCategory.deleted_at.is_(None)).order_by(BookCategory.category_name)).all()
    return success_response([{"id": str(row.id), "category_name": row.category_name, "description": row.description} for row in rows],
        "OK" if rows else "Chưa có thể loại sách trong cơ sở dữ liệu.")


@router.get("/suggested-books")
def database_books(category_id: UUID | None = Query(default=None), db: Session = Depends(get_db)) -> dict:
    query = select(SuggestedBook).where(SuggestedBook.deleted_at.is_(None))
    if category_id: query = query.where(SuggestedBook.category_id == category_id)
    rows = db.scalars(query.order_by(SuggestedBook.title)).all()
    return success_response([{"id": str(row.id), "category_id": str(row.category_id) if row.category_id else None,
        "external_book_id": row.external_book_id, "title": row.title, "author_name": row.author_name,
        "short_description": row.short_description} for row in rows], "OK" if rows else "Chưa có sách gợi ý.")
