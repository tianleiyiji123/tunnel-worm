import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


DATA_DIR = Path(os.environ.get("DATA_DIR", "./data"))
CONFIG_FILE = DATA_DIR / "config.json"


class Settings(BaseSettings):
    # Database
    DB_TYPE: str = ""  # "sqlite" or "mysql", empty = auto-detect
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "suisuichong"
    DB_PASSWORD: str = "suisuichong123"
    DB_NAME: str = "suisuichong"

    # Storage
    STORAGE_TYPE: str = "local"
    UPLOAD_DIR: str = ""

    # MinIO
    MINIO_ENDPOINT: str = ""
    MINIO_ACCESS_KEY: str = ""
    MINIO_SECRET_KEY: str = ""
    MINIO_BUCKET: str = ""
    MINIO_SECURE: bool = False

    # Aliyun OSS
    ALIOSS_ACCESS_KEY_ID: str = ""
    ALIOSS_ACCESS_KEY_SECRET: str = ""
    ALIOSS_BUCKET: str = ""
    ALIOSS_ENDPOINT: str = ""

    # Tencent COS
    TENCENTCOS_SECRET_ID: str = ""
    TENCENTCOS_SECRET_KEY: str = ""
    TENCENTCOS_BUCKET: str = ""
    TENCENTCOS_REGION: str = ""

    # Transfer settings
    TRANSFER_EXPIRE_HOURS: int = 24
    MAX_FILE_SIZE_MB: int = 50
    MAX_FILES_PER_TRANSFER: int = 10
    MAX_FAIL_ATTEMPTS: int = 5
    LOCK_DURATION_MINUTES: int = 1

    @property
    def db_url(self) -> str:
        if self.effective_db_type == "sqlite":
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            return f"sqlite:///{DATA_DIR / 'suisuichong.db'}"
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            f"?charset=utf8mb4"
        )

    @property
    def effective_db_type(self) -> str:
        """Return 'sqlite' or 'mysql' based on DB_TYPE."""
        if self.DB_TYPE in ("sqlite", "mysql"):
            return self.DB_TYPE
        # Auto-detect: if .env file loaded with a non-default DB_HOST, use mysql
        # Otherwise default to sqlite (safe for Docker fresh start)
        _env_path = Path(__file__).resolve().parent.parent / ".env"
        if _env_path.exists():
            return "mysql"
        return "sqlite"

    @property
    def upload_dir_resolved(self) -> str:
        """Return resolved upload directory path."""
        if self.UPLOAD_DIR:
            return self.UPLOAD_DIR
        return str(DATA_DIR / "uploads")

    @property
    def minio_endpoint_clean(self) -> str:
        """Return MINIO_ENDPOINT without scheme prefix (http:// or https://)."""
        ep = self.MINIO_ENDPOINT.strip()
        for prefix in ("https://", "http://"):
            if ep.lower().startswith(prefix):
                ep = ep[len(prefix):]
                break
        return ep.rstrip("/")

    # .env 文件路径：优先当前目录，其次项目根目录
    _env_file = Path(__file__).resolve().parent.parent / ".env"
    model_config = {
        "env_file": str(_env_file) if _env_file.exists() else ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
