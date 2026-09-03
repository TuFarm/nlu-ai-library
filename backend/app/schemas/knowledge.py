from pydantic import BaseModel


class MockKnowledgeUpload(BaseModel):
    file_name: str = "tai-lieu-mau.pdf"
    source_type: str = "PDF"
