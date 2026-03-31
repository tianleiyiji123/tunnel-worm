from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from database import get_db, User as UserModel, Transfer, TransferRecord, TransferFile
from schemas import RecordsResponse, RecordItem
from deps import get_current_user

router = APIRouter(prefix="/api/records", tags=["records"])


@router.get("", response_model=RecordsResponse)
async def get_records(
    action: Optional[str] = Query(None, description="Filter by action: send or retrieve"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: Optional[UserModel] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get operation records for the current user. Requires login."""
    if not user:
        raise HTTPException(status_code=401, detail="请先登录")

    query = db.query(TransferRecord).filter(TransferRecord.user_id == user.id)

    if action:
        query = query.filter(TransferRecord.action == action)

    # Count total
    total = query.count()

    # Get paginated records
    records = (
        query.order_by(TransferRecord.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    items = []
    for r in records:
        transfer = db.query(Transfer).filter(Transfer.code == r.transfer_code).first()
        file_count = 0
        if transfer and transfer.type in ("file", "mixed"):
            file_count = db.query(func.count(TransferFile.id)).filter(
                TransferFile.transfer_code == r.transfer_code
            ).scalar() or 0
        items.append(
            RecordItem(
                id=r.id,
                action=r.action,
                transfer_code=r.transfer_code,
                transfer_type=transfer.type if transfer else None,
                text_preview=transfer.text_content[:100] if transfer and transfer.text_content else None,
                file_count=file_count,
                permanent=transfer.permanent if transfer else False,
                created_at=r.created_at,
            )
        )

    return RecordsResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )
