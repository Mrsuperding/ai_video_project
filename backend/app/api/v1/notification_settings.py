"""
通知设置 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.message import UpdateNotificationSettingsRequest
from app.schemas.response import success_response
from app.services.message_service import MessageService

router = APIRouter()


@router.get("")
async def get_notification_settings(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取通知设置"""
    settings = MessageService.get_notification_settings(db, user_id)
    return success_response(settings)


@router.patch("")
async def update_notification_settings(
    request: UpdateNotificationSettingsRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """更新通知设置"""
    data = request.model_dump(exclude_unset=True)
    settings = MessageService.update_notification_settings(db, user_id, data)
    return success_response(settings)