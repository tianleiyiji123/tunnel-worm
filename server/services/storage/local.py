import os
import aiofiles
from services.storage.base import StorageBackend, FileInfo
from config import settings


class LocalStorage(StorageBackend):
    def __init__(self):
        self.base_dir = settings.upload_dir_resolved

    async def upload(self, code: str, filename: str, file_content: bytes, content_type: str) -> str:
        dir_path = os.path.join(self.base_dir, code)
        os.makedirs(dir_path, exist_ok=True)
        storage_path = os.path.join(dir_path, filename)
        async with aiofiles.open(storage_path, 'wb') as f:
            await f.write(file_content)
        return storage_path

    async def download(self, code: str, filename: str) -> tuple[bytes, str]:
        file_path = os.path.join(self.base_dir, code, filename)
        async with aiofiles.open(file_path, 'rb') as f:
            content = await f.read()
        return content, "application/octet-stream"

    async def get_download_url(self, code: str, filename: str) -> str:
        return f"/api/transfer/{code}/download/{filename}"

    async def delete(self, code: str):
        import shutil
        dir_path = os.path.join(self.base_dir, code)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    async def list_files(self, code: str) -> list[FileInfo]:
        dir_path = os.path.join(self.base_dir, code)
        if not os.path.exists(dir_path):
            return []
        files = []
        for name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, name)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                files.append(FileInfo(name=name, size=size, content_type="application/octet-stream"))
        return files

    async def ensure_bucket(self):
        os.makedirs(self.base_dir, exist_ok=True)
