import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from database import Transfer, TransferFile, TransferRecord
from config import settings


def _get_storage():
    """Lazy get storage instance."""
    from services.storage import get_storage
    return get_storage()


def generate_code(db: Session) -> str:
    """Generate a unique 4-character code (uppercase letters + digits).

    Uses uppercase letters only to avoid ambiguity between l/1, O/0, I/1.
    Excludes confusable characters: O, 0, I, 1.
    """
    # Exclude ambiguous chars: 0 (confused with O), 1 (confused with I/l), I (confused with 1), O (confused with 0)
    chars = string.ascii_uppercase.replace('O', '').replace('I', '') + string.digits.replace('0', '').replace('1', '')
    for _ in range(100):
        code = ''.join(random.choices(chars, k=4))
        exists = db.query(Transfer).filter(Transfer.code == code).first()
        if not exists:
            return code
    raise Exception("Failed to generate unique code after 100 attempts")


def create_transfer(
    db: Session,
    transfer_type: str,
    text_content: str = None,
    files: list = None,
    user_id: int = None,
) -> Transfer:
    """Create a new transfer record.

    If user_id is provided and type is text or mixed-with-text,
    the transfer is marked as permanent (never expires).
    File-only transfers always expire after TRANSFER_EXPIRE_HOURS.
    """
    code = generate_code(db)
    expires_at = datetime.utcnow() + timedelta(hours=settings.TRANSFER_EXPIRE_HOURS)

    # Determine if this transfer should be permanent
    is_permanent = False
    if user_id and transfer_type in ("text", "mixed"):
        is_permanent = True

    transfer = Transfer(
        code=code,
        type=transfer_type,
        text_content=text_content if transfer_type in ("text", "mixed") else None,
        expires_at=expires_at,
        user_id=user_id,
        permanent=is_permanent,
    )
    db.add(transfer)
    db.commit()
    db.refresh(transfer)

    # Record the send action
    record = TransferRecord(
        user_id=user_id,
        action="send",
        transfer_code=code,
    )
    db.add(record)
    db.commit()

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

    # Permanent transfers never expire
    if not transfer.permanent and transfer.expires_at < now:
        return False, "资源已过期"

    # Check lock
    if transfer.locked_until and transfer.locked_until > now:
        remaining = (transfer.locked_until - now).seconds
        return False, f"密码已锁定，请 {remaining} 秒后重试"

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


def get_transfer(db: Session, code: str, user_id: int = None, client_ip: str = None) -> Transfer:
    """Get transfer by code and increment download count. Records retrieve action."""
    transfer = db.query(Transfer).filter(Transfer.code == code).first()
    if transfer:
        transfer.download_count = (transfer.download_count or 0) + 1
        transfer.fail_count = 0
        db.commit()

        # Record retrieve action
        record = TransferRecord(
            user_id=user_id,
            action="retrieve",
            transfer_code=code,
            client_ip=client_ip,
        )
        db.add(record)
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
    """Delete expired transfers and their files.

    Permanent transfers (user's text) are never deleted.
    """
    storage = _get_storage()
    now = datetime.utcnow()
    expired = (
        db.query(Transfer)
        .filter(Transfer.expires_at < now, Transfer.permanent == False)
        .all()
    )
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
        # Delete transfer records
        db.query(TransferRecord).filter(TransferRecord.transfer_code == t.code).delete()
        # Delete transfer record
        db.delete(t)
        count += 1
    db.commit()
    if count > 0:
        print(f"🧹 Cleaned up {count} expired transfers")
