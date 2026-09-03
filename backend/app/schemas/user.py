from uuid import UUID

from pydantic import BaseModel


class UserRead(BaseModel):
    id: UUID
    student_code: str
    full_name: str
    email: str
    phone: str | None = None
    user_type: str
    account_status: str


class UserProfileRead(UserRead):
    faculty: str | None = None
    major: str | None = None
    admission_year: int | None = None
    calculated_student_year: int | None = None
    preferred_language: str = "vi"


class MockCurrentUserResponse(BaseModel):
    success: bool = True
    message: str = "OK"
    data: UserProfileRead
