from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db, User as UserModel
from schemas import TransferCreateResponse, TransferVerifyRequest, TransferResponse
from services import transfer_service
from config import settings
from deps import get_current_user

router = APIRouter(prefix="/api/transfer", tags=["transfer"])


@router.get("/reserve-code")
async def reserve_code(db: Session = Depends(get_db)):
    """Reserve a unique 4-character code for E2EE encryption.

    Creates a placeholder Transfer record so the code is locked.
    The client should encrypt content with this code, then call
    create_transfer with encrypted data and the same code.
    """
    code = transfer_service.reserve_code(db)
    return {"code": code}


@router.post("", response_model=TransferCreateResponse)
async def create_transfer(
    type: str = Form(...),
    text_content: Optional[str] = Form(None),
    files: List[UploadFile] = File(default=[]),
    encrypted: bool = Form(False),
    salt: Optional[str] = Form(None),
    iv: Optional[str] = Form(None),
    reserved_code: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    user: Optional[UserModel] = Depends(get_current_user),
):
    """Upload text and/or files, create a transfer with a 4-character code."""
    # Validate type
    if type not in ("text", "file", "mixed"):
        raise HTTPException(status_code=400, detail="类型必须为 text、file 或 mixed")

    # Validate content
    if type == "text" and not text_content:
        raise HTTPException(status_code=400, detail="请输入文本内容")
    if type == "file" and not files:
        raise HTTPException(status_code=400, detail="请至少上传一个文件")
    if type == "mixed" and (not text_content and not files):
        raise HTTPException(status_code=400, detail="请输入文本或上传文件")

    # Validate file limits
    if len(files) > settings.MAX_FILES_PER_TRANSFER:
        raise HTTPException(
            status_code=400,
            detail=f"最多上传 {settings.MAX_FILES_PER_TRANSFER} 个文件",
        )
    for f in files:
        content = await f.read()
        await f.seek(0)
        size_mb = len(content) / (1024 * 1024)
        if size_mb > settings.MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=f"文件 {f.filename} 超过 {settings.MAX_FILE_SIZE_MB}MB 限制",
            )

    # Determine actual type
    actual_type = type
    if type == "mixed" and not text_content:
        actual_type = "file"
    elif type == "mixed" and not files:
        actual_type = "text"

    # Get user_id if logged in
    user_id = user.id if user else None

    # Create transfer (with optional user_id for permanent text saving)
    transfer = transfer_service.create_transfer(
        db, actual_type, text_content, user_id=user_id,
        encrypted=encrypted, salt=salt, iv=iv,
        reserved_code=reserved_code,
    )

    # Save files if any
    if files:
        await transfer_service.save_files(db, transfer, files)

    return TransferCreateResponse(
        code=transfer.code,
        type=transfer.type,
        expires_at=transfer.expires_at,
    )


@router.post("/verify")
async def verify_code(req: TransferVerifyRequest, db: Session = Depends(get_db)):
    """Verify if a code is valid before retrieving."""
    if not req.code or len(req.code) < 4:
        raise HTTPException(status_code=400, detail="请输入完整的密码")

    valid, msg = transfer_service.verify_code(db, req.code)
    if not valid:
        # Record the failed attempt
        _, fail_msg = transfer_service.record_fail(db, req.code)
        return {"valid": False, "message": fail_msg}
    return {"valid": True, "message": ""}


@router.get("/{code}", response_model=TransferResponse)
async def get_transfer(
    code: str,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[UserModel] = Depends(get_current_user),
):
    """Retrieve transfer details by code."""
    if len(code) < 4:
        raise HTTPException(status_code=400, detail="请输入完整的密码")

    valid, msg = transfer_service.verify_code(db, code)
    if not valid:
        transfer_service.record_fail(db, code)
        raise HTTPException(status_code=404, detail=msg)

    # Get client IP
    client_ip = request.client.host if request.client else None
    user_id = user.id if user else None

    transfer = transfer_service.get_transfer(db, code, user_id=user_id, client_ip=client_ip)
    if not transfer:
        raise HTTPException(status_code=404, detail="密码无效")

    files_info = []
    if transfer.type in ("file", "mixed"):
        files_info = await transfer_service.get_transfer_files_info(db, transfer)

    return TransferResponse(
        code=transfer.code,
        type=transfer.type,
        text_content=transfer.text_content if transfer.type in ("text", "mixed") else None,
        files=files_info if files_info else None,
        created_at=transfer.created_at,
        expires_at=transfer.expires_at,
        download_count=transfer.download_count or 0,
        encrypted=transfer.encrypted or False,
        salt=transfer.salt,
        iv=transfer.iv,
    )


@router.get("/{code}/download/{filename}")
async def download_file(code: str, filename: str, db: Session = Depends(get_db)):
    """Download a specific file from a transfer."""
    valid, msg = transfer_service.verify_code(db, code)
    if not valid:
        raise HTTPException(status_code=404, detail=msg)

    try:
        content, content_type = await transfer_service.get_file_content(code, filename)
        return Response(
            content=content,
            media_type=content_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="文件不存在")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载失败: {str(e)}")
