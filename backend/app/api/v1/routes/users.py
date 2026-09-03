from uuid import UUID
from fastapi import APIRouter
from app.core.responses import success_response
from app.schemas.user import MockCurrentUserResponse, UserProfileRead
from app.services.user_service import calculate_student_year

router = APIRouter()

@router.get("/me/mock", response_model=MockCurrentUserResponse)
async def mock_current_user() -> dict:
    admission_year = 2024
    user = UserProfileRead(id=UUID("d8f8b7db-56b5-4be5-a136-19eb154ae21f"), student_code="ITCSIU24092",
        full_name="Phạm Hoàng Tuấn Tú", email="tu.pham@example.edu.vn", phone="0901234567", user_type="student",
        faculty="Công nghệ thông tin", major="Khoa học máy tính", admission_year=admission_year,
        calculated_student_year=calculate_student_year(admission_year), account_status="active", preferred_language="vi")
    return success_response(user.model_dump(mode="json"))
