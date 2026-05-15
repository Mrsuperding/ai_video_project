"""
消息相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MessageItem(BaseModel):
    """消息列表项"""
    id: int
    message_type: str
    title: str
    content: Optional[str] = None
    action_url: Optional[str] = None
    action_text: Optional[str] = None
    related_type: Optional[str] = None
    related_id: Optional[int] = None
    is_read: bool = False
    created_at: datetime


class UnreadCountResponse(BaseModel):
    """未读消息数响应"""
    unread_count: int


class MarkReadRequest(BaseModel):
    """标记已读请求"""
    message_ids: Optional[List[int]] = None


class NotificationSettingsResponse(BaseModel):
    """通知设置响应"""
    notify_task_complete: bool = True
    notify_task_failed: bool = True
    notify_review_result: bool = True
    notify_system: bool = True
    email_enabled: bool = True
    email_task_complete: bool = False
    email_task_failed: bool = True
    email_payment: bool = True
    email_security: bool = True
    sms_enabled: bool = False
    sms_payment: bool = False
    sms_security: bool = True


class UpdateNotificationSettingsRequest(BaseModel):
    """更新通知设置请求"""
    notify_task_complete: Optional[bool] = None
    notify_task_failed: Optional[bool] = None
    notify_review_result: Optional[bool] = None
    notify_system: Optional[bool] = None
    email_enabled: Optional[bool] = None
    email_task_complete: Optional[bool] = None
    email_task_failed: Optional[bool] = None
    email_payment: Optional[bool] = None
    email_security: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    sms_payment: Optional[bool] = None
    sms_security: Optional[bool] = None