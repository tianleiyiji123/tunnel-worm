import oss2
from io import BytesIO
from services.storage.base import StorageBackend, FileInfo
from config import settings


class AliOssStorage(StorageBackend):
    def __init__(self):
        auth = oss2.Auth(settings.ALIOSS_ACCESS_KEY_ID, settings.ALIOSS_ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(auth, settings.ALIOSS_ENDPOINT, settings.ALIOSS_BUCKET)

    async def upload(self, code: str, filename: str, file_content: bytes, content_type: str) -> str:
        storage_path = f"{code}/{filename}"
        self.bucket.put_object(storage_path, BytesIO(file_content), headers={"Content-Type": content_type})
        return storage_path

    async def download(self, code: str, filename: str) -> tuple[bytes, str]:
        storage_path = f"{code}/{filename}"
        result = self.bucket.get_object(storage_path)
        content = result.read()
        return content, result.headers.get("Content-Type", "application/octet-stream")

    async def get_download_url(self, code: str, filename: str) -> str:
        storage_path = f"{code}/{filename}"
        url = self.bucket.sign_url("GET", storage_path, 3600)
        return url

    async def delete(self, code: str):
        for obj in oss2.ObjectIterator(self.bucket, prefix=f"{code}/"):
            self.bucket.delete_object(obj.key)

    async def list_files(self, code: str) -> list[FileInfo]:
        files = []
        for obj in oss2.ObjectIterator(self.bucket, prefix=f"{code}/"):
            name = obj.key.split(f"{code}/", 1)[-1]
            if name:
                head = self.bucket.head_object(obj.key)
                files.append(FileInfo(name=name, size=head.content_length, content_type=head.content_type or "application/octet-stream"))
        return files

    async def ensure_bucket(self):
        if not self.bucket.bucket_exists:
            self.bucket.create_bucket(oss2.BUCKET_ACL_PRIVATE)
