from pydantic import BaseModel


class PDFRequest(BaseModel):
    file_name: str
    file_data: str  # Base64 encoded string


class ChatRequest(BaseModel):
    body: str
    refer: list[int]
