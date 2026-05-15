"""
消息相关模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, Text, Index, Float, JSON
from sqlalchemy.sql import func
from app.database import Base


class ContentReview(Base):
    """内容审核记录表"""
    __tablename__ = "content_reviews"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")

    target_type = Column(Enum("digital_human", "video", "script", "image"), nullable=False, comment="审核对象类型")
    target_id = Column(BigInteger, nullable=False, comment="审核对象ID")

    review_type = Column(Enum("auto", "manual"), nullable=False, default="auto", comment="审核类型")

    risk_score = Column(Float, nullable=True, comment="风险分数 0-1")
    risk_labels = Column(JSON, nullable=True, comment="风险标签列表")

    submit_data = Column(JSON, nullable=True, comment="提交的原始数据")

    result = Column(Enum("pending", "approved", "rejected"), nullable=False, default="pending", comment="审核结果")
    reviewer_id = Column(BigInteger, nullable=True, comment="审核员ID")
    review_comment = Column(String(500), nullable=True, comment="审核备注")

    created_at = Column(DateTime, server_default=func.now())
    reviewed_at = Column(DateTime, nullable=True, comment="审核时间")

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_target", "target_type", "target_id"),
        Index("idx_result", "result"),
        Index("idx_created_at", "created_at"),
    )


class UserMessage(Base):
    """用户消息表"""
    __tablename__ = "user_messages"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")

    message_type = Column(Enum("system", "task_complete", "task_failed", "review_result", "payment", "security", "other"), nullable=False, comment="消息类型")
    title = Column(String(200), nullable=False, comment="标题")
    content = Column(Text, nullable=True, comment="内容")
    action_url = Column(String(500), nullable=True, comment="跳转链接")
    action_text = Column(String(50), nullable=True, comment="链接文字")

    related_type = Column(String(50), nullable=True, comment="关联类型")
    related_id = Column(BigInteger, nullable=True, comment="关联ID")

    is_read = Column(Enum("0", "1"), default="0", comment="是否已读")
    read_at = Column(DateTime, nullable=True, comment="阅读时间")

    push_sent = Column(Enum("0", "1"), default="0", comment="是否已推送")
    email_sent = Column(Enum("0", "1"), default="0", comment="是否已发送邮件")
    sms_sent = Column(Enum("0", "1"), default="0", comment="是否已发送短信")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id_read", "user_id", "is_read"),
        Index("idx_type", "message_type"),
        Index("idx_created_at", "created_at"),
    )


class UserNotificationSettings(Base):
    """用户通知设置表"""
    __tablename__ = "user_notification_settings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, unique=True, comment="用户ID")

    notify_task_complete = Column(Enum("0", "1"), default="1", comment="任务完成通知")
    notify_task_failed = Column(Enum("0", "1"), default="1", comment="任务失败通知")
    notify_review_result = Column(Enum("0", "1"), default="1", comment="审核结果通知")
    notify_system = Column(Enum("0", "1"), default="1", comment="系统公告通知")

    email_enabled = Column(Enum("0", "1"), default="1", comment="邮件通知总开关")
    email_task_complete = Column(Enum("0", "1"), default="0", comment="任务完成(邮件)")
    email_task_failed = Column(Enum("0", "1"), default="1", comment="任务失败(邮件)")
    email_payment = Column(Enum("0", "1"), default="1", comment="支付相关(邮件)")
    email_security = Column(Enum("0", "1"), default="1", comment="安全相关(邮件)")

    sms_enabled = Column(Enum("0", "1"), default="0", comment="短信通知总开关")
    sms_payment = Column(Enum("0", "1"), default="0", comment="支付相关(短信)")
    sms_security = Column(Enum("0", "1"), default="1", comment="安全相关(短信)")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
    )