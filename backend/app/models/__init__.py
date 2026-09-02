"""Import registry for the optimized 24-table AI kiosk schema."""

from app.models.schema import *

__all__ = [name for name in globals() if not name.startswith("_")]
