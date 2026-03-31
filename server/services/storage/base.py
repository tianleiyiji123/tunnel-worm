from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FileInfo:
    name: str
    size: int
    content_type: str


class StorageBackend(ABC):
    @abstractmethod
    async def upload(self, code: str, filename: str, file_content: bytes, content_type: str) -> str:
        """Upload file, return storage path/key"""

    @abstractmethod
    async def download(self, code: str, filename: str) -> tuple[bytes, str]:
        """Download file, return (content, content_type)"""

    @abstractmethod
    async def get_download_url(self, code: str, filename: str) -> str:
        """Get download URL. Local storage returns API path, cloud returns presigned URL"""

    @abstractmethod
    async def delete(self, code: str):
        """Delete all files under the given code"""

    @abstractmethod
    async def list_files(self, code: str) -> list[FileInfo]:
        """List all files under the given code"""

    @abstractmethod
    async def ensure_bucket(self):
        """Ensure bucket/directory exists (called on startup)"""
