import os
import json
import secrets
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

    # JWT settings
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 168  # 7 days

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
        # Auto-detect: if MySQL credentials are configured (non-default), use mysql
        # Otherwise default to sqlite (safe for Docker fresh start)
        if self.DB_HOST and self.DB_HOST != "localhost":
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


def _load_config_json() -> dict:
    """Load config.json if it exists."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


# Apply config.json on startup (overrides .env values)
_cfg_json = _load_config_json()
if _cfg_json:
    # Database
    if "db_type" in _cfg_json:
        settings.DB_TYPE = _cfg_json["db_type"]
    if "db_host" in _cfg_json:
        settings.DB_HOST = _cfg_json["db_host"]
    if "db_port" in _cfg_json:
        settings.DB_PORT = _cfg_json["db_port"]
    if "db_user" in _cfg_json:
        settings.DB_USER = _cfg_json["db_user"]
    if "db_password" in _cfg_json:
        settings.DB_PASSWORD = _cfg_json["db_password"]
    if "db_name" in _cfg_json:
        settings.DB_NAME = _cfg_json["db_name"]
    # Storage
    if "storage_type" in _cfg_json:
        settings.STORAGE_TYPE = _cfg_json["storage_type"]
    if "upload_dir" in _cfg_json:
        settings.UPLOAD_DIR = _cfg_json["upload_dir"]
    # MinIO
    if "minio_endpoint" in _cfg_json:
        settings.MINIO_ENDPOINT = _cfg_json["minio_endpoint"]
    if "minio_access_key" in _cfg_json:
        settings.MINIO_ACCESS_KEY = _cfg_json["minio_access_key"]
    if "minio_secret_key" in _cfg_json:
        settings.MINIO_SECRET_KEY = _cfg_json["minio_secret_key"]
    if "minio_bucket" in _cfg_json:
        settings.MINIO_BUCKET = _cfg_json["minio_bucket"]
    if "minio_secure" in _cfg_json:
        settings.MINIO_SECURE = _cfg_json["minio_secure"]
    # Aliyun OSS
    if "alioss_access_key_id" in _cfg_json:
        settings.ALIOSS_ACCESS_KEY_ID = _cfg_json["alioss_access_key_id"]
    if "alioss_access_key_secret" in _cfg_json:
        settings.ALIOSS_ACCESS_KEY_SECRET = _cfg_json["alioss_access_key_secret"]
    if "alioss_bucket" in _cfg_json:
        settings.ALIOSS_BUCKET = _cfg_json["alioss_bucket"]
    if "alioss_endpoint" in _cfg_json:
        settings.ALIOSS_ENDPOINT = _cfg_json["alioss_endpoint"]
    # Tencent COS
    if "tencentcos_secret_id" in _cfg_json:
        settings.TENCENTCOS_SECRET_ID = _cfg_json["tencentcos_secret_id"]
    if "tencentcos_secret_key" in _cfg_json:
        settings.TENCENTCOS_SECRET_KEY = _cfg_json["tencentcos_secret_key"]
    if "tencentcos_bucket" in _cfg_json:
        settings.TENCENTCOS_BUCKET = _cfg_json["tencentcos_bucket"]
    if "tencentcos_region" in _cfg_json:
        settings.TENCENTCOS_REGION = _cfg_json["tencentcos_region"]

# Generate a temporary JWT_SECRET if still empty (will be persisted on startup)
if not settings.JWT_SECRET:
    settings.JWT_SECRET = secrets.token_urlsafe(32)
