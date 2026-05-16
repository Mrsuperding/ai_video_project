"""
数字人相关模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, JSON, Text, DECIMAL, Index, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base


class DigitalHuman(Base):
    """数字人表"""
    __tablename__ = "digital_humans"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    name = Column(String(100), nullable=False, comment="数字人名称")
    description = Column(Text, nullable=True, comment="描述")

    source_type = Column(Enum("single_photo", "multi_photos", "video"), default="single_photo", comment="源类型")
    source_photos = Column(JSON, nullable=True, comment="源照片信息")
    photo_count = Column(BigInteger, nullable=True, comment="照片数量")

    gender = Column(Enum("male", "female", "unknown"), nullable=True, comment="性别")
    age_group = Column(Enum("child", "young", "middle", "senior"), nullable=True, comment="年龄段")
    skin_tone = Column(Enum("light", "medium", "dark"), nullable=True, comment="肤色")

    hairstyle_id = Column(BigInteger, nullable=True, comment="发型配置ID")
    clothing_type = Column(Enum("business", "casual", "formal", "custom"), nullable=True, comment="服装类型")
    clothing_url = Column(String(500), nullable=True, comment="自定义服装图URL")
    accessories = Column(JSON, nullable=True, comment="配饰")
    background_type = Column(Enum("transparent", "color", "scene", "custom"), nullable=True, comment="背景类型")
    background_value = Column(String(50), nullable=True, comment="背景值")

    status = Column(Enum("pending", "processing", "completed", "failed", "deleted"), default="pending", comment="生成状态")
    model_version = Column(String(50), nullable=True, comment="模型版本")
    model_provider = Column(String(50), nullable=True, comment="模型提供商")

    model_file_url = Column(String(500), nullable=True, comment="数字人模型文件URL")
    preview_image_url = Column(String(500), nullable=True, comment="静态预览图URL")
    preview_video_url = Column(String(500), nullable=True, comment="动态预览视频URL")
    preview_video_duration = Column(DECIMAL(5, 2), nullable=True, comment="预览视频时长(秒)")

    authorization_type = Column(Enum("self", "others", "public"), nullable=False, comment="授权类型")
    authorization_status = Column(Enum("auto_approved", "pending", "approved", "rejected"), default="auto_approved", comment="授权审核状态")
    authorization_proof_url = Column(String(500), nullable=True, comment="授权证明文件URL")
    authorization_reject_reason = Column(String(255), nullable=True, comment="驳回原因")
    authorization_expire_at = Column(DateTime, nullable=True, comment="授权到期时间")

    usage_count = Column(BigInteger, default=0, comment="使用次数")
    is_default = Column(Boolean, default=False, comment="是否为默认数字人")

    parent_id = Column(BigInteger, nullable=True, comment="父版本ID")
    version_number = Column(BigInteger, default=1, comment="版本号")

    error_message = Column(Text, nullable=True, comment="生成失败原因")
    retry_count = Column(BigInteger, default=0, comment="重试次数")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True, comment="软删除时间")

    __table_args__ = (
        Index("idx_digital_humans_user_id", "user_id"),
        Index("idx_digital_humans_status", "status"),
        Index("idx_authorization", "authorization_type", "authorization_status"),
        Index("idx_digital_humans_idx_usage_count", "usage_count"),
    )


class DigitalHumanTask(Base):
    """数字人生成任务表"""
    __tablename__ = "digital_human_tasks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    digital_human_id = Column(BigInteger, nullable=True, comment="数字人ID")
    human_name = Column(String(100), nullable=False, comment="数字人名称")

    task_type = Column(Enum("create", "update", "retrain"), nullable=False, comment="任务类型")
    status = Column(Enum("queued", "processing", "completed", "failed", "cancelled"), default="queued", comment="任务状态")
    priority = Column(BigInteger, default=5, comment="优先级")

    model_provider = Column(String(50), nullable=False, comment="提供商")
    model_name = Column(String(100), nullable=False, comment="模型名称")
    model_version = Column(String(50), nullable=True, comment="模型版本")

    input_config = Column(JSON, nullable=False, comment="输入配置")

    progress = Column(BigInteger, default=0, comment="进度 0-100")
    current_step = Column(String(50), nullable=True, comment="当前步骤")

    output_config = Column(JSON, nullable=True, comment="输出结果")
    model_file_url = Column(String(500), nullable=True, comment="模型文件URL")
    preview_image_url = Column(String(500), nullable=True, comment="预览图URL")
    preview_video_url = Column(String(500), nullable=True, comment="预览视频URL")

    started_at = Column(DateTime, nullable=True, comment="开始处理时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    duration_seconds = Column(BigInteger, nullable=True, comment="处理耗时(秒)")
    cost_cents = Column(BigInteger, nullable=True, comment="成本(分)")

    error_code = Column(String(50), nullable=True, comment="错误代码")
    error_message = Column(Text, nullable=True, comment="错误信息")
    retry_count = Column(BigInteger, default=0, comment="重试次数")
    max_retries = Column(BigInteger, default=3, comment="最大重试次数")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_digital_human_tasks_user_id", "user_id"),
        Index("idx_digital_human_tasks_digital_human_id", "digital_human_id"),
        Index("idx_digital_human_tasks_status", "status", "priority"),
        Index("idx_digital_human_tasks_created_at", "created_at"),
    )