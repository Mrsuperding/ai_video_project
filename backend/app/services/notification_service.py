"""
通知服务
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime

from app.models.message import UserMessage, UserNotificationSettings
from app.core.websocket_manager import manager


class NotificationService:
    """通知服务"""

    @staticmethod
    def send_task_complete_notification(
        db: Session,
        user_id: int,
        project_id: int,
        project_name: str,
        video_url: str = None
    ):
        """发送任务完成通知"""
        # 检查用户通知设置
        settings = db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == user_id
        ).first()

        if settings and settings.notify_task_complete == "0":
            return

        # 创建消息
        message = UserMessage(
            user_id=user_id,
            message_type="task_complete",
            title="视频生成完成",
            content=f"您的视频「{project_name}」已生成完成",
            action_url=f"/projects/{project_id}",
            action_text="查看视频",
            related_type="video_project",
            related_id=project_id
        )
        db.add(message)
        db.commit()

        # 通过 WebSocket 推送
        from app.core.websocket_manager import manager
        import asyncio
        asyncio.create_task(
            manager.send_personal_message(user_id, {
                "type": "task_completed",
                "data": {
                    "message_id": message.id,
                    "message_type": "task_complete",
                    "title": message.title,
                    "content": message.content
                }
            })
        )

    @staticmethod
    def send_task_failed_notification(
        db: Session,
        user_id: int,
        project_id: int,
        project_name: str,
        error_message: str = None
    ):
        """发送任务失败通知"""
        settings = db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == user_id
        ).first()

        if settings and settings.notify_task_failed == "0":
            return

        content = f"您的视频「{project_name}」生成失败"
        if error_message:
            content += f": {error_message}"

        message = UserMessage(
            user_id=user_id,
            message_type="task_failed",
            title="视频生成失败",
            content=content,
            action_url=f"/projects/{project_id}",
            action_text="查看详情",
            related_type="video_project",
            related_id=project_id
        )
        db.add(message)
        db.commit()

        # 通过 WebSocket 推送
        import asyncio
        asyncio.create_task(
            manager.send_personal_message(user_id, {
                "type": "task_failed",
                "data": {
                    "message_id": message.id,
                    "message_type": "task_failed",
                    "title": message.title,
                    "content": message.content
                }
            })
        )

    @staticmethod
    def send_review_notification(
        db: Session,
        user_id: int,
        target_type: str,
        target_id: int,
        result: str,
        reason: str = None
    ):
        """发送审核结果通知"""
        settings = db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == user_id
        ).first()

        if settings and settings.notify_review_result == "0":
            return

        if result == "approved":
            title = "审核通过"
            content = f"您的{target_type}已审核通过"
        else:
            title = "审核未通过"
            content = f"您的{target_type}未通过审核"
            if reason:
                content += f": {reason}"

        message = UserMessage(
            user_id=user_id,
            message_type="review_result",
            title=title,
            content=content,
            action_url=f"/{target_type}s/{target_id}",
            action_text="查看详情",
            related_type=target_type,
            related_id=target_id
        )
        db.add(message)
        db.commit()

    @staticmethod
    def push_task_progress(
        user_id: int,
        task_id: int,
        task_type: str,
        project_id: int,
        progress: int,
        current_step: str,
        estimated_seconds: int = None
    ):
        """推送任务进度"""
        import asyncio
        asyncio.create_task(
            manager.send_personal_message(user_id, {
                "type": "task_progress",
                "data": {
                    "task_id": task_id,
                    "task_type": task_type,
                    "project_id": project_id,
                    "progress": progress,
                    "current_step": current_step,
                    "estimated_seconds": estimated_seconds
                }
            })
        )