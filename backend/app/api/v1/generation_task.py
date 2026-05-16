"""
生成任务 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.response import success_response, error_response
from app.services.video_service import VideoService
from app.core.exceptions import NotFoundException

router = APIRouter()


@router.get("/task/{task_id}")
def get_generation_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取任务状态"""
    try:
        task = VideoService.get_generation_task(db, user_id, task_id)
        return success_response(task)
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.get("/tasks")
def get_tasks(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取任务列表"""
    return success_response({"items": []})