"""
统计相关模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Date, Enum, DECIMAL, Index
from sqlalchemy.sql import func
from app.database import Base


class UserStatistics(Base):
    """用户统计表"""
    __tablename__ = "user_statistics"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")

    stat_date = Column(Date, nullable=False, comment="统计日期")
    stat_type = Column(Enum("daily", "weekly", "monthly"), nullable=False, comment="统计类型")

    video_projects_created = Column(BigInteger, default=0, comment="创建项目数")
    video_projects_completed = Column(BigInteger, default=0, comment="完成项目数")
    video_projects_failed = Column(BigInteger, default=0, comment="失败项目数")
    video_total_duration = Column(BigInteger, default=0, comment="总视频时长(秒)")

    digital_humans_created = Column(BigInteger, default=0, comment="创建数字人数")
    digital_humans_used = Column(BigInteger, default=0, comment="使用数字人次数")

    cost_cents = Column(BigInteger, default=0, comment="总消费(分)")

    storage_used_mb = Column(BigInteger, default=0, comment="已用存储(MB)")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_user_statistics_stat_date", "stat_date"),
    )


class PlatformStatistics(Base):
    """平台统计表"""
    __tablename__ = "platform_statistics"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    stat_date = Column(Date, nullable=False, comment="统计日期")
    stat_hour = Column(BigInteger, nullable=True, comment="统计小时")

    new_users = Column(BigInteger, default=0, comment="新增用户")
    active_users = Column(BigInteger, default=0, comment="活跃用户")
    paid_users = Column(BigInteger, default=0, comment="付费用户")
    churned_users = Column(BigInteger, default=0, comment="流失用户")

    video_projects_created = Column(BigInteger, default=0, comment="创建项目数")
    video_projects_completed = Column(BigInteger, default=0, comment="完成项目数")
    video_projects_failed = Column(BigInteger, default=0, comment="失败项目数")
    video_total_duration = Column(BigInteger, default=0, comment="总视频时长(秒)")

    digital_humans_created = Column(BigInteger, default=0, comment="创建数字人数")
    ai_tasks_submitted = Column(BigInteger, default=0, comment="提交AI任务数")
    ai_tasks_completed = Column(BigInteger, default=0, comment="完成AI任务数")

    total_revenue_cents = Column(BigInteger, default=0, comment="总收入(分)")
    membership_revenue_cents = Column(BigInteger, default=0, comment="会员收入(分)")
    single_purchase_revenue_cents = Column(BigInteger, default=0, comment="单次购买收入(分)")

    total_cost_cents = Column(BigInteger, default=0, comment="总成本(分)")
    model_cost_cents = Column(BigInteger, default=0, comment="AI模型成本(分)")
    storage_cost_cents = Column(BigInteger, default=0, comment="存储成本(分)")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_platform_statistics_date_hour", "stat_date", "stat_hour"),
        Index("idx_platform_statistics_stat_date", "stat_date"),
    )


class ModelUsageStatistics(Base):
    """模型调用统计表"""
    __tablename__ = "model_usage_statistics"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    stat_date = Column(Date, nullable=False, comment="统计日期")
    stat_hour = Column(BigInteger, nullable=True, comment="统计小时")

    model_provider = Column(String(50), nullable=False, comment="提供商")
    model_name = Column(String(100), nullable=False, comment="模型名称")
    model_task_type = Column(Enum("digital_human", "video_gen", "tts", "ai_writing"), nullable=False, comment="任务类型")

    call_count = Column(BigInteger, default=0, comment="调用次数")
    success_count = Column(BigInteger, default=0, comment="成功次数")
    fail_count = Column(BigInteger, default=0, comment="失败次数")
    timeout_count = Column(BigInteger, default=0, comment="超时次数")

    avg_duration_ms = Column(BigInteger, default=0, comment="平均耗时(毫秒)")
    p50_duration_ms = Column(BigInteger, default=0, comment="P50耗时")
    p95_duration_ms = Column(BigInteger, default=0, comment="P95耗时")
    p99_duration_ms = Column(BigInteger, default=0, comment="P99耗时")

    total_cost_cents = Column(BigInteger, default=0, comment="总成本(分)")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_model_usage_statistics_date_provider_model", "stat_date", "stat_hour", "model_provider", "model_name", "model_task_type"),
        Index("idx_model_usage_statistics_stat_date", "stat_date"),
    )