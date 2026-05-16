"""
消息服务
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.message import UserMessage, UserNotificationSettings
from app.core.exceptions import NotFoundException


class MessageService:
    """消息服务"""

    @staticmethod
    def get_messages(
        db: Session,
        user_id: int,
        is_read: bool = None,
        message_type: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取消息列表"""
        query = db.query(UserMessage).filter(UserMessage.user_id == user_id)

        if is_read is not None:
            query = query.filter(UserMessage.is_read == ("1" if is_read else "0"))

        if message_type:
            query = query.filter(UserMessage.message_type == message_type)

        total = query.count()
        unread_count = db.query(UserMessage).filter(
            UserMessage.user_id == user_id,
            UserMessage.is_read == "0"
        ).count()

        items = query.order_by(
            UserMessage.created_at.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "items": [
                {
                    "id": m.id,
                    "message_type": m.message_type,
                    "title": m.title,
                    "content": m.content,
                    "action_url": m.action_url,
                    "action_text": m.action_text,
                    "related_type": m.related_type,
                    "related_id": m.related_id,
                    "is_read": m.is_read == True,
                    "created_at": m.created_at
                }
                for m in items
            ],
            "unread_count": unread_count,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }

    @staticmethod
    def get_unread_count(db: Session, user_id: int) -> int:
        """获取未读消息数"""
        return db.query(UserMessage).filter(
            UserMessage.user_id == user_id,
            UserMessage.is_read == "0"
        ).count()

    @staticmethod
    def mark_read(db: Session, user_id: int, message_id: int) -> bool:
        """标记已读"""
        message = db.query(UserMessage).filter(
            UserMessage.id == message_id,
            UserMessage.user_id == user_id
        ).first()

        if message:
            message.is_read = "1"
            message.read_at = datetime.utcnow()
            db.commit()
        return True

    @staticmethod
    def mark_all_read(db: Session, user_id: int) -> bool:
        """标记全部已读"""
        db.query(UserMessage).filter(
            UserMessage.user_id == user_id,
            UserMessage.is_read == "0"
        ).update({
            "is_read": "1",
            "read_at": datetime.utcnow()
        })
        db.commit()
        return True

    @staticmethod
    def delete_message(db: Session, user_id: int, message_id: int) -> bool:
        """删除消息"""
        message = db.query(UserMessage).filter(
            UserMessage.id == message_id,
            UserMessage.user_id == user_id
        ).first()

        if message:
            db.delete(message)
            db.commit()
        return True

    @staticmethod
    def get_notification_settings(db: Session, user_id: int) -> Dict[str, Any]:
        """获取通知设置"""
        settings = db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == user_id
        ).first()

        if not settings:
            settings = UserNotificationSettings(user_id=user_id)
            db.add(settings)
            db.commit()
            db.refresh(settings)

        return {
            "notify_task_complete": settings.notify_task_complete == True,
            "notify_task_failed": settings.notify_task_failed == True,
            "notify_review_result": settings.notify_review_result == True,
            "notify_system": settings.notify_system == True,
            "email_enabled": settings.email_enabled == True,
            "email_task_complete": settings.email_task_complete == True,
            "email_task_failed": settings.email_task_failed == True,
            "email_payment": settings.email_payment == True,
            "email_security": settings.email_security == True,
            "sms_enabled": settings.sms_enabled == True,
            "sms_payment": settings.sms_payment == True,
            "sms_security": settings.sms_security == True
        }

    @staticmethod
    def update_notification_settings(
        db: Session,
        user_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """更新通知设置"""
        settings = db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == user_id
        ).first()

        if not settings:
            settings = UserNotificationSettings(user_id=user_id)
            db.add(settings)

        for key, value in data.items():
            if value is not None and hasattr(settings, key):
                setattr(settings, key, "1" if value else "0")

        settings.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(settings)

        return MessageService.get_notification_settings(db, user_id)

    @staticmethod
    def create_message(
        db: Session,
        user_id: int,
        message_type: str,
        title: str,
        content: str = None,
        action_url: str = None,
        action_text: str = None,
        related_type: str = None,
        related_id: int = None
    ) -> UserMessage:
        """创建消息"""
        message = UserMessage(
            user_id=user_id,
            message_type=message_type,
            title=title,
            content=content,
            action_url=action_url,
            action_text=action_text,
            related_type=related_type,
            related_id=related_id
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message