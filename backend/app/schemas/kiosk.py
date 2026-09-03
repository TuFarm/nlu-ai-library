from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class KioskSessionStart(BaseModel):
    device_code: str = Field(default="KIOSK_DEV_01", min_length=2, max_length=80)
    mode: Literal["kiosk"] = "kiosk"


class KioskSessionEnd(BaseModel):
    exit_reason: str = Field(default="COMPLETED", max_length=40)


class KioskEventCreate(BaseModel):
    event_type: str = Field(min_length=2, max_length=80)
    input_method: str | None = Field(default=None, max_length=30)
    content_summary: str | None = Field(default=None, max_length=2000)
    success: bool = True
