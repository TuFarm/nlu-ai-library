from pydantic import BaseModel


class SuggestedBookRead(BaseModel):
    external_book_id: str | None
    title: str
    author_name: str
    category: str
