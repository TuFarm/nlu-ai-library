from fastapi import APIRouter, Query
from app.core.responses import success_response

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
