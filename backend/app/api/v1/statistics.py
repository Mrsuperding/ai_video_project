"""
统计 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.response import success_response
from app.models.user import User
from app.models.video import VideoProject, VideoOutput
from app.models.digital_human import DigitalHuman
from app.services.wallet_service import WalletService

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
    # 实际查询数据
    from sqlalchemy import func

    # 视频项目统计
    video_projects_created = db.query(func.count(VideoProject.id)).filter(
        VideoProject.user_id == user_id
    ).scalar() or 0

    completed = db.query(func.count(VideoOutput.id)).join(VideoProject).filter(
        VideoProject.user_id == user_id,
        VideoOutput.id.isnot(None)
    ).scalar() or 0

    return success_response({
        "period": period,
        "start_date": start_date or (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
        "end_date": end_date or datetime.now().strftime("%Y-%m-%d"),
        "video_projects": {
            "created": video_projects_created,
            "completed": completed,
            "failed": 0,
            "total_duration": 0,
            "avg_duration": 0.0
        },
        "digital_humans": {
            "created": 0,
            "used": 0
        },
        "cost": {
            "total_cents": 0,
            "avg_per_video_cents": 0
        },
        "storage": {
            "used_mb": 0,
            "quota_mb": 10240,
            "usage_percent": 0.0
        },
        "quota": {
            "digital_human": {"total": 100, "used": 2, "remaining": 98},
            "video_monthly": {"total": 500, "used": video_projects_created, "remaining": 500 - video_projects_created}
        }
    })


@router.get("/quota")
async def get_quota(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取配额使用情况"""
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