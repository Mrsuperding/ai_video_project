"""
统计 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.response import success_response

router = APIRouter()


@router.get("")
async def get_user_statistics(
    period: str = "monthly",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取用户使用统计"""
    return success_response({
        "period": period,
        "start_date": start_date or "2024-01-01",
        "end_date": end_date or "2024-01-31",
        "video_projects": {
            "created": 15,
            "completed": 12,
            "failed": 1,
            "total_duration": 540,
            "avg_duration": 45.0
        },
        "digital_humans": {
            "created": 2,
            "used": 18
        },
        "cost": {
            "total_cents": 650,
            "avg_per_video_cents": 54.17
        },
        "storage": {
            "used_mb": 2048,
            "quota_mb": 10240,
            "usage_percent": 20.0
        },
        "quota": {
            "digital_human": {"total": 100, "used": 2, "remaining": 98},
            "video_monthly": {"total": 500, "used": 15, "remaining": 485}
        }
    })


@router.get("/quota")
async def get_quota(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取配额使用情况"""
    from app.models.user import User
    from app.services.wallet_service import WalletService

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return success_response({
            "digital_human": {"total": 3, "used": 0, "remaining": 3, "reset_at": None},
            "video_monthly": {"total": 10, "used": 0, "remaining": 10, "reset_at": None},
            "video_max_duration": 60,
            "storage_mb": {"total": 1024, "used": 0, "remaining": 1024}
        })

    quota = WalletService.calculate_quota(db, user)
    return success_response(quota)