from qcloud_cos import CosConfig, CosS3Client
from qcloud_cos.cos_exception import CosServiceError
from io import BytesIO
from services.storage.base import StorageBackend, FileInfo
from config import settings


class TencentCosStorage(StorageBackend):
    def __init__(self):
        config = CosConfig(
            Region=settings.TENCENTCOS_REGION,
            SecretId=settings.TENCENTCOS_SECRET_ID,
            SecretKey=settings.TENCENTCOS_SECRET_KEY,
        )
        self.client = CosS3Client(config)
        self.bucket = settings.TENCENTCOS_BUCKET

    async def upload(self, code: str, filename: str, file_content: bytes, content_type: str) -> str:
        storage_path = f"{code}/{filename}"
        self.client.put_object(
            Bucket=self.bucket,
            Body=BytesIO(file_content),
            Key=storage_path,
            ContentType=content_type,
        )
        return storage_path

    async def download(self, code: str, filename: str) -> tuple[bytes, str]:
        storage_path = f"{code}/{filename}"
        response = self.client.get_object(Bucket=self.bucket, Key=storage_path)
        content = response["Body"].read()
        ct = response.get("ContentType", "application/octet-stream")
        return content, ct

    async def get_download_url(self, code: str, filename: str) -> str:
        storage_path = f"{code}/{filename}"
        url = self.client.get_presigned_url(
            Method="GET",
            Bucket=self.bucket,
            Key=storage_path,
            Expired=3600,
        )
        return url

    async def delete(self, code: str):
        resp = self.client.list_objects(Bucket=self.bucket, Prefix=f"{code}/")
        if "Contents" in resp:
            objects = [{"Key": obj["Key"]} for obj in resp["Contents"]]
            if objects:
                self.client.delete_objects(Bucket=self.bucket, Delete={"Object": objects})

    async def list_files(self, code: str) -> list[FileInfo]:
        files = []
        resp = self.client.list_objects(Bucket=self.bucket, Prefix=f"{code}/")
        if "Contents" in resp:
            for obj in resp["Contents"]:
                name = obj["Key"].split(f"{code}/", 1)[-1]
                if name:
                    files.append(FileInfo(name=name, size=obj["Size"], content_type="application/octet-stream"))
        return files

    async def ensure_bucket(self):
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except CosServiceError:
            self.client.create_bucket(Bucket=self.bucket, ACL="private")
