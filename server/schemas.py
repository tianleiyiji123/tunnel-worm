from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ---- Transfer Schemas ----

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
    encrypted: bool = False
    salt: Optional[str] = None
    iv: Optional[str] = None


class TransferCreateResponse(BaseModel):
    code: str
    type: str
    expires_at: datetime


# ---- Auth Schemas ----

class UserRegisterRequest(BaseModel):
    username: str
    password: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    token: str


# ---- Records Schemas ----

class RecordItem(BaseModel):
    id: int
    action: str  # "send" or "retrieve"
    transfer_code: str
    transfer_type: Optional[str] = None
    text_preview: Optional[str] = None
    file_count: int = 0
    permanent: bool = False
    created_at: datetime


class RecordsResponse(BaseModel):
    items: List[RecordItem]
    total: int
    page: int
    page_size: int
