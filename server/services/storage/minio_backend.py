from minio import Minio
from io import BytesIO
from services.storage.base import StorageBackend, FileInfo
from config import settings


class MinIOStorage(StorageBackend):
    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint_clean,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self.bucket = settings.MINIO_BUCKET

    async def upload(self, code: str, filename: str, file_content: bytes, content_type: str) -> str:
        storage_path = f"{code}/{filename}"
        self.client.put_object(
            self.bucket,
            storage_path,
            BytesIO(file_content),
            length=len(file_content),
            content_type=content_type,
        )
        return storage_path

    async def download(self, code: str, filename: str) -> tuple[bytes, str]:
        storage_path = f"{code}/{filename}"
        response = self.client.get_object(self.bucket, storage_path)
        content = response.read()
        response.close()
        response.release_conn()
        return content, "application/octet-stream"

    async def get_download_url(self, code: str, filename: str) -> str:
        from datetime import timedelta
        storage_path = f"{code}/{filename}"
        url = self.client.presigned_get_object(
            self.bucket, storage_path, expires=timedelta(hours=1)
        )
        return url

    async def delete(self, code: str):
        objects = self.client.list_objects(self.bucket, prefix=f"{code}/")
        for obj in objects:
            self.client.remove_object(self.bucket, obj.object_name)

    async def list_files(self, code: str) -> list[FileInfo]:
        objects = self.client.list_objects(self.bucket, prefix=f"{code}/")
        files = []
        for obj in objects:
            name = obj.object_name.split(f"{code}/", 1)[-1]
            if name:
                stat = self.client.stat_object(self.bucket, obj.object_name)
                files.append(FileInfo(name=name, size=stat.size, content_type=stat.content_type or "application/octet-stream"))
        return files

    async def ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)
