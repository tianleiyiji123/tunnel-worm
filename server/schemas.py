from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TransferCreateRequest(BaseModel):
    type: str  # "text", "file", or "mixed"
    text_content: Optional[str] = None


class TransferVerifyRequest(BaseModel):
    code: str


class FileInfoResponse(BaseModel):
    name: str
    size: int
    content_type: str
    download_url: str


class TransferResponse(BaseModel):
    code: str
    type: str
    text_content: Optional[str] = None
    files: Optional[List[FileInfoResponse]] = None
    created_at: datetime
    expires_at: datetime
    download_count: int


class TransferCreateResponse(BaseModel):
    code: str
    type: str
    expires_at: datetime
