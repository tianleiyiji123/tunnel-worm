from services.storage.base import StorageBackend
from services.storage.local import LocalStorage
from config import settings

# 懒加载映射：存储类型 -> (模块路径, 类名)
_LAZY_STORAGE_MAP = {
    "minio": ("services.storage.minio_backend", "MinIOStorage"),
    "alioss": ("services.storage.alioss", "AliOssStorage"),
    "tencentcos": ("services.storage.tencentcos", "TencentCosStorage"),
}


def _detect_storage_type() -> str:
    """Auto-detect storage backend by checking which credentials are configured."""
    # Check Aliyun OSS
    if all([
        settings.ALIOSS_ACCESS_KEY_ID,
        settings.ALIOSS_ACCESS_KEY_SECRET,
        settings.ALIOSS_BUCKET,
        settings.ALIOSS_ENDPOINT,
    ]):
        return "alioss"

    # Check Tencent COS
    if all([
        settings.TENCENTCOS_SECRET_ID,
        settings.TENCENTCOS_SECRET_KEY,
        settings.TENCENTCOS_BUCKET,
        settings.TENCENTCOS_REGION,
    ]):
        return "tencentcos"

    # Check MinIO
    if all([
        settings.MINIO_ENDPOINT,
        settings.MINIO_ACCESS_KEY,
        settings.MINIO_SECRET_KEY,
        settings.MINIO_BUCKET,
    ]):
        return "minio"

    return "local"


def get_storage() -> StorageBackend:
    """Factory function to get storage backend.

    Priority: explicit STORAGE_TYPE env var > auto-detect credentials > local.
    Uses lazy import for third-party SDKs to avoid ImportError when not installed.
    """
    storage_type = settings.STORAGE_TYPE.lower().strip()
    auto_detected = False

    if storage_type in ("", "auto", "local"):
        storage_type = _detect_storage_type()
        auto_detected = True

    if storage_type == "local":
        print("📦 Storage backend: local")
        return LocalStorage()

    if storage_type not in _LAZY_STORAGE_MAP:
        print(f"⚠️  Unknown STORAGE_TYPE '{storage_type}', falling back to local")
        return LocalStorage()

    # Lazy import to avoid ImportError when SDK is not installed
    module_path, class_name = _LAZY_STORAGE_MAP[storage_type]
    try:
        import importlib
        module = importlib.import_module(module_path)
        storage_class = getattr(module, class_name)
        source = "auto-detected" if auto_detected else "configured"
        print(f"📦 Storage backend: {storage_type} ({source})")
        return storage_class()
    except ImportError as e:
        print(f"⚠️  Failed to import {storage_type} SDK ({e}), falling back to local")
        return LocalStorage()
