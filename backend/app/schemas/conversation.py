from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    text: str = Field(min_length=1, max_length=4000)


class ConversationStart(BaseModel):
    session_id: UUID | None = None
    user_id: UUID | None = None


class ConversationMessageCreate(BaseModel):
    sender_type: Literal["USER", "ASSISTANT", "SYSTEM"] = "USER"
    message_text: str = Field(min_length=1, max_length=4000)
    input_method: Literal["TEXT", "VOICE", "SYSTEM"] = "TEXT"
