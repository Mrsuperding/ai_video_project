"""
依赖注入
"""
from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config import settings
from app.database import get_db

security = HTTPBearer()


def get_current_user_id(token: str = Depends(security)) -> int:
    """从 token 获取当前用户 ID"""
    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 20003, "message": "Invalid token"}
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 20003, "message": "Invalid token"}
        )


def get_current_admin_id(token: str = Depends(security)) -> int:
    """从 token 获取当前管理员 ID"""
    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        admin_id: int = payload.get("admin_id")
        if admin_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 20003, "message": "Invalid token"}
            )
        return admin_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 20003, "message": "Invalid token"}
        )


async def get_current_user(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取当前用户完整信息"""
    from app.models.user import User
    user = db.query(User).filter(User.id == user_id, User.status == "active").first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 20006, "message": "Account deleted"}
        )
    return user