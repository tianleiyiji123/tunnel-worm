import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import Transfer, TransferFile
from config import settings


def _get_storage():
    """Lazy get storage instance."""
    from services.storage import get_storage
    return get_storage()


def generate_code(db: Session) -> str:
    """Generate a unique 4-digit code."""
    for _ in range(100):
        code = f"{random.randint(0, 9999):04d}"
        exists = db.query(Transfer).filter(Transfer.code == code).first()
        if not exists:
            return code
    raise Exception("Failed to generate unique code after 100 attempts")


def create_transfer(db: Session, transfer_type: str, text_content: str = None, files: list = None) -> Transfer:
    """Create a new transfer record."""
    code = generate_code(db)
    expires_at = datetime.utcnow() + timedelta(hours=settings.TRANSFER_EXPIRE_HOURS)

    transfer = Transfer(
        code=code,
        type=transfer_type,
        text_content=text_content if transfer_type in ("text", "mixed") else None,
        expires_at=expires_at,
    )
    db.add(transfer)
    db.commit()
    db.refresh(transfer)
    return transfer


async def save_files(db: Session, transfer: Transfer, uploaded_files: list):
    """Save uploaded files to storage and create file records."""
    storage = _get_storage()
    for file in uploaded_files:
        content = await file.read()
        storage_path = await storage.upload(transfer.code, file.filename, content, file.content_type)
        file_record = TransferFile(
            transfer_code=transfer.code,
            original_name=file.filename,
            storage_path=storage_path,
            file_size=len(content),
            content_type=file.content_type,
        )
        db.add(file_record)
    db.commit()


def verify_code(db: Session, code: str) -> tuple[bool, str]:
    """Verify a code is valid (not expired, not locked, exists)."""
    transfer = db.query(Transfer).filter(Transfer.code == code).first()

    if not transfer:
        return False, "密码无效，请检查后重试"

    now = datetime.utcnow()

    # Check lock
    if transfer.locked_until and transfer.locked_until > now:
        remaining = (transfer.locked_until - now).seconds
        return False, f"密码已锁定，请 {remaining} 秒后重试"

    # Check expiry
    if transfer.expires_at < now:
        return False, "资源已过期"

    # Reset fail count if unlocked
    if transfer.locked_until and transfer.locked_until <= now:
        transfer.fail_count = 0
        transfer.locked_until = None
        db.commit()

    return True, ""


def record_fail(db: Session, code: str) -> tuple[bool, str]:
    """Record a failed attempt. Returns (locked, message)."""
    transfer = db.query(Transfer).filter(Transfer.code == code).first()
    if not transfer:
        return False, "密码无效，请检查后重试"

    transfer.fail_count = (transfer.fail_count or 0) + 1

    if transfer.fail_count >= settings.MAX_FAIL_ATTEMPTS:
        transfer.locked_until = datetime.utcnow() + timedelta(minutes=settings.LOCK_DURATION_MINUTES)
        db.commit()
        return True, f"错误次数过多，密码已锁定 {settings.LOCK_DURATION_MINUTES} 分钟"

    db.commit()
    remaining = settings.MAX_FAIL_ATTEMPTS - transfer.fail_count
    return False, f"密码错误，还可尝试 {remaining} 次"


def get_transfer(db: Session, code: str) -> Transfer:
    """Get transfer by code and increment download count."""
    transfer = db.query(Transfer).filter(Transfer.code == code).first()
    if transfer:
        transfer.download_count = (transfer.download_count or 0) + 1
        transfer.fail_count = 0
        db.commit()
    return transfer


async def get_transfer_files_info(db: Session, transfer: Transfer) -> list[dict]:
    """Get file info with download URLs for a transfer."""
    storage = _get_storage()
    files = db.query(TransferFile).filter(TransferFile.transfer_code == transfer.code).all()
    result = []
    for f in files:
        download_url = await storage.get_download_url(transfer.code, f.original_name)
        result.append({
            "name": f.original_name,
            "size": f.file_size,
            "content_type": f.content_type,
            "download_url": download_url,
        })
    return result


async def get_file_content(code: str, filename: str) -> tuple[bytes, str]:
    """Get file content for download."""
    storage = _get_storage()
    return await storage.download(code, filename)


def cleanup_expired(db: Session):
    """Delete expired transfers and their files."""
    storage = _get_storage()
    now = datetime.utcnow()
    expired = db.query(Transfer).filter(Transfer.expires_at < now).all()
    count = 0
    for t in expired:
        # Delete files from storage (sync context in cleanup)
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.ensure_future(storage.delete(t.code))
            else:
                loop.run_until_complete(storage.delete(t.code))
        except RuntimeError:
            pass

        # Delete file records
        db.query(TransferFile).filter(TransferFile.transfer_code == t.code).delete()
        # Delete transfer record
        db.delete(t)
        count += 1
    db.commit()
    if count > 0:
        print(f"🧹 Cleaned up {count} expired transfers")
