"""安装向导配置管理模块。

负责 config.json 的读写、应用配置的热更新。
"""
import json
from pathlib import Path
from typing import Optional
from config import CONFIG_FILE, DATA_DIR, settings


def is_initialized() -> bool:
    """Check if the application has been initialized (config.json exists)."""
    return CONFIG_FILE.exists()


def load_config() -> dict:
    """Load config from config.json if it exists."""
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config: dict):
    """Save config to config.json."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def apply_config(config: dict):
    """Apply config values to the global settings object.

    This updates settings in-place so that the rest of the application
    picks up the new values without restart.
    """
    # Database settings
    if "db_type" in config:
        settings.DB_TYPE = config["db_type"]
    if "db_host" in config:
        settings.DB_HOST = config["db_host"]
    if "db_port" in config:
        settings.DB_PORT = config["db_port"]
    if "db_user" in config:
        settings.DB_USER = config["db_user"]
    if "db_password" in config:
        settings.DB_PASSWORD = config["db_password"]
    if "db_name" in config:
        settings.DB_NAME = config["db_name"]

    # Storage settings
    if "storage_type" in config:
        settings.STORAGE_TYPE = config["storage_type"]
    if "upload_dir" in config:
        settings.UPLOAD_DIR = config["upload_dir"]

    # MinIO
    if "minio_endpoint" in config:
        settings.MINIO_ENDPOINT = config["minio_endpoint"]
    if "minio_access_key" in config:
        settings.MINIO_ACCESS_KEY = config["minio_access_key"]
    if "minio_secret_key" in config:
        settings.MINIO_SECRET_KEY = config["minio_secret_key"]
    if "minio_bucket" in config:
        settings.MINIO_BUCKET = config["minio_bucket"]
    if "minio_secure" in config:
        settings.MINIO_SECURE = config["minio_secure"]

    # Aliyun OSS
    if "alioss_access_key_id" in config:
        settings.ALIOSS_ACCESS_KEY_ID = config["alioss_access_key_id"]
    if "alioss_access_key_secret" in config:
        settings.ALIOSS_ACCESS_KEY_SECRET = config["alioss_access_key_secret"]
    if "alioss_bucket" in config:
        settings.ALIOSS_BUCKET = config["alioss_bucket"]
    if "alioss_endpoint" in config:
        settings.ALIOSS_ENDPOINT = config["alioss_endpoint"]

    # Tencent COS
    if "tencentcos_secret_id" in config:
        settings.TENCENTCOS_SECRET_ID = config["tencentcos_secret_id"]
    if "tencentcos_secret_key" in config:
        settings.TENCENTCOS_SECRET_KEY = config["tencentcos_secret_key"]
    if "tencentcos_bucket" in config:
        settings.TENCENTCOS_BUCKET = config["tencentcos_bucket"]
    if "tencentcos_region" in config:
        settings.TENCENTCOS_REGION = config["tencentcos_region"]


def reset_db_engine():
    """Force recreate database engine with current settings.

    Must be called after apply_config() when switching database type.
    """
    import database
    database._engine = None
    database._SessionLocal = None
