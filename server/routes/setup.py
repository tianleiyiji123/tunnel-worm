"""安装向导 API 路由。

提供首次启动的配置向导接口：
- GET  /api/setup/status   → 检查是否已初始化
- POST /api/setup/test-db  → 测试数据库连接
- POST /api/setup/test-storage → 测试存储连通性
- POST /api/setup/finish   → 完成安装，写入配置
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from setup_config import is_initialized, save_config, apply_config, reset_db_engine

router = APIRouter(prefix="/api/setup", tags=["setup"])


# ---- Request/Response Schemas ----

class SetupStatusResponse(BaseModel):
    initialized: bool


class TestDbRequest(BaseModel):
    db_type: str  # "sqlite" or "mysql"
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_name: Optional[str] = None


class TestStorageRequest(BaseModel):
    storage_type: str  # "local", "minio", "alioss", "tencentcos"
    minio_endpoint: Optional[str] = None
    minio_access_key: Optional[str] = None
    minio_secret_key: Optional[str] = None
    minio_bucket: Optional[str] = None
    alioss_access_key_id: Optional[str] = None
    alioss_access_key_secret: Optional[str] = None
    alioss_bucket: Optional[str] = None
    alioss_endpoint: Optional[str] = None
    tencentcos_secret_id: Optional[str] = None
    tencentcos_secret_key: Optional[str] = None
    tencentcos_bucket: Optional[str] = None
    tencentcos_region: Optional[str] = None


class SetupFinishRequest(BaseModel):
    db_type: str
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_name: Optional[str] = None
    storage_type: str
    upload_dir: Optional[str] = None
    minio_endpoint: Optional[str] = None
    minio_access_key: Optional[str] = None
    minio_secret_key: Optional[str] = None
    minio_bucket: Optional[str] = None
    minio_secure: Optional[bool] = None
    alioss_access_key_id: Optional[str] = None
    alioss_access_key_secret: Optional[str] = None
    alioss_bucket: Optional[str] = None
    alioss_endpoint: Optional[str] = None
    tencentcos_secret_id: Optional[str] = None
    tencentcos_secret_key: Optional[str] = None
    tencentcos_bucket: Optional[str] = None
    tencentcos_region: Optional[str] = None


# ---- Endpoints ----

@router.get("/status", response_model=SetupStatusResponse)
async def setup_status():
    """Check if the application has been initialized."""
    return SetupStatusResponse(initialized=is_initialized())


def _guard_already_initialized():
    """Reject requests if already initialized."""
    if is_initialized():
        raise HTTPException(status_code=403, detail="系统已完成初始化，无法修改配置")


@router.post("/test-db")
async def test_db(req: TestDbRequest):
    """Test database connection with the provided settings."""
    _guard_already_initialized()

    try:
        if req.db_type == "sqlite":
            from config import DATA_DIR
            from sqlalchemy import create_engine
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            db_path = DATA_DIR / "suisuichong.db"
            url = f"sqlite:///{db_path}"
            engine = create_engine(url, connect_args={"check_same_thread": False})
            with engine.connect():
                pass
            engine.dispose()
            return {"success": True, "message": "SQLite 连接测试成功"}
        else:
            from sqlalchemy import create_engine
            url = (
                f"mysql+pymysql://{req.db_user}:{req.db_password}"
                f"@{req.db_host}:{req.db_port}/{req.db_name}"
                f"?charset=utf8mb4"
            )
            engine = create_engine(url, pool_recycle=3600, pool_pre_ping=True)
            with engine.connect():
                pass
            engine.dispose()
            return {"success": True, "message": "MySQL 连接测试成功"}
    except Exception as e:
        return {"success": False, "message": f"连接失败: {str(e)}"}


@router.post("/test-storage")
async def test_storage(req: TestStorageRequest):
    """Test storage backend connectivity."""
    _guard_already_initialized()

    try:
        if req.storage_type == "local":
            return {"success": True, "message": "本地存储无需测试，始终可用"}
        elif req.storage_type == "minio":
            from minio import Minio
            import urllib3
            urllib3.disable_warnings()
            endpoint = req.minio_endpoint or ""
            if endpoint.startswith("http://"):
                secure = False
                endpoint = endpoint[7:]
            elif endpoint.startswith("https://"):
                secure = True
                endpoint = endpoint[8:]
            else:
                secure = False
            client = Minio(
                endpoint,
                access_key=req.minio_access_key or "",
                secret_key=req.minio_secret_key or "",
                secure=secure,
            )
            if not client.bucket_exists(req.minio_bucket or ""):
                client.make_bucket(req.minio_bucket or "")
            return {"success": True, "message": "MinIO 连接测试成功"}
        elif req.storage_type == "alioss":
            import oss2
            auth = oss2.Auth(
                req.alioss_access_key_id or "",
                req.alioss_access_key_secret or "",
            )
            bucket = oss2.Bucket(auth, req.alioss_endpoint or "", req.alioss_bucket or "")
            bucket.head_bucket()
            return {"success": True, "message": "阿里云 OSS 连接测试成功"}
        elif req.storage_type == "tencentcos":
            from qcloud_cos import CosConfig, CosS3Client
            import json
            token = None
            conf = CosConfig(
                Region=req.tencentcos_region or "",
                SecretId=req.tencentcos_secret_id or "",
                SecretKey=req.tencentcos_secret_key or "",
                Token=token,
                Scheme="https",
            )
            client = CosS3Client(conf)
            client.head_bucket(Bucket=req.tencentcos_bucket or "")
            return {"success": True, "message": "腾讯云 COS 连接测试成功"}
        else:
            return {"success": False, "message": f"不支持的存储类型: {req.storage_type}"}
    except ImportError:
        return {"success": False, "message": "缺少对应的存储 SDK，请安装依赖后重试"}
    except Exception as e:
        return {"success": False, "message": f"连接失败: {str(e)}"}


@router.post("/finish")
async def setup_finish(req: SetupFinishRequest):
    """Save configuration and initialize the system."""
    _guard_already_initialized()

    # Build config dict
    config = {"db_type": req.db_type, "storage_type": req.storage_type}

    if req.db_type == "mysql":
        if not all([req.db_host, req.db_user, req.db_password, req.db_name]):
            raise HTTPException(status_code=400, detail="MySQL 模式需填写完整数据库连接信息")
        config.update({
            "db_host": req.db_host,
            "db_port": req.db_port or 3306,
            "db_user": req.db_user,
            "db_password": req.db_password,
            "db_name": req.db_name,
        })

    if req.upload_dir:
        config["upload_dir"] = req.upload_dir

    # Storage config
    if req.storage_type == "minio":
        if not all([req.minio_endpoint, req.minio_access_key, req.minio_secret_key, req.minio_bucket]):
            raise HTTPException(status_code=400, detail="MinIO 模式需填写完整凭证信息")
        config.update({
            "minio_endpoint": req.minio_endpoint,
            "minio_access_key": req.minio_access_key,
            "minio_secret_key": req.minio_secret_key,
            "minio_bucket": req.minio_bucket,
            "minio_secure": req.minio_secure or False,
        })
    elif req.storage_type == "alioss":
        if not all([req.alioss_access_key_id, req.alioss_access_key_secret, req.alioss_bucket, req.alioss_endpoint]):
            raise HTTPException(status_code=400, detail="阿里云 OSS 模式需填写完整凭证信息")
        config.update({
            "alioss_access_key_id": req.alioss_access_key_id,
            "alioss_access_key_secret": req.alioss_access_key_secret,
            "alioss_bucket": req.alioss_bucket,
            "alioss_endpoint": req.alioss_endpoint,
        })
    elif req.storage_type == "tencentcos":
        if not all([req.tencentcos_secret_id, req.tencentcos_secret_key, req.tencentcos_bucket, req.tencentcos_region]):
            raise HTTPException(status_code=400, detail="腾讯云 COS 模式需填写完整凭证信息")
        config.update({
            "tencentcos_secret_id": req.tencentcos_secret_id,
            "tencentcos_secret_key": req.tencentcos_secret_key,
            "tencentcos_bucket": req.tencentcos_bucket,
            "tencentcos_region": req.tencentcos_region,
        })

    # Save to config.json
    save_config(config)

    # Apply config to running settings
    apply_config(config)

    # Reset and initialize database
    reset_db_engine()
    from database import init_db
    init_db()

    # Initialize storage
    from services.storage import get_storage
    storage = get_storage()
    await storage.ensure_bucket()

    return {"success": True, "message": "配置保存成功，系统初始化完成"}
