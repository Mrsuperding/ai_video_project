"""
API 依赖
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user_id, get_current_user, get_current_admin_id


def get_current_user(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取当前登录用户"""
    return get_current_user(db, user_id)


def get_admin(
    admin_id: int = Depends(get_current_admin_id)
) -> int:
    """获取当前管理员"""
    return admin_id