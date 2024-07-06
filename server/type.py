from pydantic import BaseModel
from typing import Any


class PDFRequest(BaseModel):
    file_name: str
    file_data: str  # Base64 encoded string

class PaperPatchRequest(BaseModel):
    raw: str

class ChatRequest(BaseModel):
    body: str
    refer: list[int]

class MarkRequest(BaseModel):
    marks: list[Any]

class TranslationApi(BaseModel):
    raw: str