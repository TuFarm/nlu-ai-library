from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    text: str = Field(min_length=1, max_length=4000)


class ConversationStart(BaseModel):
    session_id: str | None = None
