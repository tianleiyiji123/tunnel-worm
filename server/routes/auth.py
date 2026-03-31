from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
)
from services import auth_service
from deps import get_current_user
from database import User as UserModel
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(req: UserRegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    if not req.username or len(req.username) < 2:
        raise HTTPException(status_code=400, detail="用户名至少 2 个字符")
    if len(req.username) > 50:
        raise HTTPException(status_code=400, detail="用户名最多 50 个字符")
    if not req.password or len(req.password) < 4:
        raise HTTPException(status_code=400, detail="密码至少 4 个字符")

    try:
        user = auth_service.create_user(db, req.username, req.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = auth_service.create_token(user.id)
    return UserResponse(
        id=user.id,
        username=user.username,
        token=token,
    )


@router.post("/login", response_model=UserResponse)
async def login(req: UserLoginRequest, db: Session = Depends(get_db)):
    """Login with username and password."""
    user = auth_service.authenticate_user(db, req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = auth_service.create_token(user.id)
    return UserResponse(
        id=user.id,
        username=user.username,
        token=token,
    )


@router.get("/me")
async def get_me(user: Optional[UserModel] = Depends(get_current_user)):
    """Get current user info. Returns null if not logged in."""
    if not user:
        return {"user": None}
    return {
        "user": {
            "id": user.id,
            "username": user.username,
        }
    }
