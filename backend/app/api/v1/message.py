"""
消息 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.message import *
from app.schemas.response import success_response, error_response
from app.services.message_service import MessageService

router = APIRouter()


@router.get("")
async def get_messages(
    is_read: Optional[bool] = None,
    message_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取消息列表"""
    result = MessageService.get_messages(db, user_id, is_read, message_type, page, page_size)
    return success_response(result)


@router.get("/unread-count")
async def get_unread_count(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取未读消息数"""
    count = MessageService.get_unread_count(db, user_id)
    return success_response({"unread_count": count})


@router.post("/{message_id}/read")
async def mark_read(
    message_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """标记已读"""
    MessageService.mark_read(db, user_id, message_id)
    return success_response(message="标记成功")


@router.post("/read-all")
async def mark_all_read(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """标记全部已读"""
    MessageService.mark_all_read(db, user_id)
    return success_response(message="标记成功")


@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """删除消息"""
    MessageService.delete_message(db, user_id, message_id)
    return success_response(message="删除成功")


# 通知设置
@router.get("/settings")
async def get_notification_settings(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取通知设置"""
    settings = MessageService.get_notification_settings(db, user_id)
    return success_response(settings)


@router.patch("/settings")
async def update_notification_settings(
    request: UpdateNotificationSettingsRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """更新通知设置"""
    data = request.model_dump(exclude_unset=True)
    settings = MessageService.update_notification_settings(db, user_id, data)
    return success_response(settings)