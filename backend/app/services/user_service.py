"""Small user-domain helpers."""
from datetime import UTC, datetime


def calculate_student_year(
    admission_year: int | None, current_year: int | None = None
) -> int | None:
    """Return the 1-based study year, or None for missing/future admission years."""
    if admission_year is None:
        return None
    effective_year = current_year if current_year is not None else datetime.now(UTC).year
    if admission_year > effective_year:
        return None
    return effective_year - admission_year + 1
