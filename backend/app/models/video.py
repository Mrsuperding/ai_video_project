"""
视频相关模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, JSON, Text, DECIMAL, Index, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base


class VideoProject(Base):
    """视频项目表"""
    __tablename__ = "video_projects"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    project_name = Column(String(200), nullable=False, comment="项目名称")
    description = Column(Text, nullable=True, comment="项目描述")

    resolution = Column(Enum("720p", "1080p", "2k", "4k"), default="1080p", comment="分辨率")
    aspect_ratio = Column(String(20), default="16:9", comment="宽高比")
    fps = Column(BigInteger, default=30, comment="帧率")
    max_duration = Column(BigInteger, nullable=True, comment="最大时长(秒)")

    digital_human_id = Column(BigInteger, ForeignKey("digital_humans.id", ondelete="RESTRICT"), nullable=False, comment="主数字人ID")
    digital_human_config = Column(JSON, nullable=True, comment="数字人配置")

    script_id = Column(BigInteger, ForeignKey("scripts.id", ondelete="RESTRICT"), nullable=False, comment="脚本ID")
    script_content = Column(JSON, nullable=True, comment="脚本内容快照")

    voice_id = Column(BigInteger, ForeignKey("voice_clones.id", ondelete="SET NULL"), nullable=True, comment="TTS音色ID")
    tts_config = Column(JSON, nullable=True, comment="TTS配置")

    background_asset_id = Column(BigInteger, ForeignKey("user_assets.id", ondelete="SET NULL"), nullable=True, comment="背景素材ID")
    background_type = Column(Enum("color", "image", "video", "transparent"), default="image", comment="背景类型")
    background_value = Column(String(100), nullable=True, comment="背景值")

    bgm_asset_id = Column(BigInteger, ForeignKey("user_assets.id", ondelete="SET NULL"), nullable=True, comment="背景音乐素材ID")
    bgm_volume = Column(DECIMAL(3, 2), default=0.30, comment="BGM音量")

    timeline_config = Column(JSON, nullable=True, comment="时间线配置")
    subtitle_config = Column(JSON, nullable=True, comment="字幕配置")

    tags = Column(JSON, nullable=True, comment="标签")
    category = Column(String(50), nullable=True, comment="分类")

    generation_status = Column(Enum("draft", "queued", "preprocessing", "generating", "postprocessing", "quality_check", "completed", "failed"), default="draft", comment="生成状态")
    model_provider = Column(String(50), nullable=True, comment="模型提供商")
    model_name = Column(String(100), nullable=True, comment="模型名称")
    priority = Column(BigInteger, default=5, comment="优先级")

    view_count = Column(BigInteger, default=0, comment="查看次数")
    download_count = Column(BigInteger, default=0, comment="下载次数")
    share_count = Column(BigInteger, default=0, comment="分享次数")

    cost_cents = Column(BigInteger, nullable=True, comment="实际成本(分)")

    deleted_at = Column(DateTime, nullable=True, comment="软删除时间")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_video_projects_user_id", "user_id"),
        Index("idx_video_projects_digital_human_id", "digital_human_id"),
        Index("idx_video_projects_script_id", "script_id"),
        Index("idx_video_projects_status_time", "generation_status", "created_at"),
        Index("idx_video_projects_created_at", "created_at"),
    )


class VideoOutput(Base):
    """视频输出表"""
    __tablename__ = "video_outputs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(BigInteger, ForeignKey("video_projects.id", ondelete="CASCADE"), nullable=False, unique=True, comment="项目ID")

    video_url = Column(String(500), nullable=False, comment="视频文件URL")
    video_path = Column(String(500), nullable=True, comment="视频存储路径")
    thumbnail_url = Column(String(500), nullable=True, comment="缩略图URL")
    video_file_size = Column(BigInteger, nullable=True, comment="视频文件大小")

    resolution = Column(String(20), nullable=True, comment="分辨率")
    duration = Column(DECIMAL(8, 2), nullable=True, comment="实际时长(秒)")
    fps = Column(BigInteger, nullable=True, comment="帧率")
    codec = Column(String(50), nullable=True, comment="编码")
    bitrate = Column(BigInteger, nullable=True, comment="码率")
    has_audio = Column(Boolean, default=True, comment="是否有音频")

    quality_score = Column(BigInteger, nullable=True, comment="质量评分")
    review_status = Column(Enum("pending", "approved", "rejected", "auto_approved", "auto_rejected"), default="auto_approved", comment="审核状态")
    review_reason = Column(String(255), nullable=True, comment="审核原因")

    watermark_embedded = Column(Boolean, default=False, comment="是否嵌入水印")
    c2pa_manifest_url = Column(String(500), nullable=True, comment="C2PA清单文件URL")

    share_token = Column(String(100), nullable=True, comment="分享Token")
    share_enabled = Column(Boolean, default=False, comment="是否启用分享")
    share_expire_at = Column(DateTime, nullable=True, comment="分享过期时间")
    share_password = Column(String(50), nullable=True, comment="分享密码")

    view_count = Column(BigInteger, default=0, comment="查看次数")
    download_count = Column(BigInteger, default=0, comment="下载次数")
    share_count = Column(BigInteger, default=0, comment="分享次数")

    expires_at = Column(DateTime, nullable=True, comment="过期时间")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_video_outputs_review_status", "review_status"),
        Index("idx_video_outputs_created_at", "created_at"),
    )


class GenerationTask(Base):
    """生成任务表"""
    __tablename__ = "generation_tasks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    project_id = Column(BigInteger, ForeignKey("video_projects.id", ondelete="CASCADE"), nullable=False, comment="项目ID")
    batch_id = Column(String(100), nullable=True, comment="批次ID")

    task_type = Column(Enum("tts", "video_gen", "postprocess", "quality_check", "full_pipeline"), nullable=False, comment="任务类型")

    status = Column(Enum("queued", "processing", "completed", "failed", "cancelled"), default="queued", comment="状态")
    priority = Column(BigInteger, default=5, comment="优先级")
    queue_position = Column(BigInteger, nullable=True, comment="队列位置")

    progress = Column(BigInteger, default=0, comment="进度 0-100")
    current_step = Column(String(50), nullable=True, comment="当前步骤")

    model_provider = Column(String(50), nullable=True, comment="提供商")
    model_name = Column(String(100), nullable=True, comment="模型名称")
    model_version = Column(String(50), nullable=True, comment="模型版本")

    input_config = Column(JSON, nullable=True, comment="输入配置")

    output_config = Column(JSON, nullable=True, comment="输出配置")
    output_urls = Column(JSON, nullable=True, comment="输出文件URLs")

    estimated_duration = Column(BigInteger, nullable=True, comment="预估时长(秒)")
    started_at = Column(DateTime, nullable=True, comment="开始时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    duration_seconds = Column(BigInteger, nullable=True, comment="实际耗时(秒)")
    cost_cents = Column(BigInteger, nullable=True, comment="成本(分)")

    retry_count = Column(BigInteger, default=0, comment="重试次数")
    max_retries = Column(BigInteger, default=3, comment="最大重试次数")
    retry_from_provider = Column(String(50), nullable=True, comment="上次失败的提供商")
    fallback_provider = Column(String(50), nullable=True, comment="切换到的提供商")

    error_code = Column(String(50), nullable=True, comment="错误代码")
    error_message = Column(Text, nullable=True, comment="错误信息")
    is_timeout = Column(Boolean, default=False, comment="是否超时")

    logs = Column(JSON, nullable=True, comment="详细日志")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_generation_tasks_user_id", "user_id"),
        Index("idx_generation_tasks_project_id", "project_id"),
        Index("idx_generation_tasks_status_priority", "status", "priority"),
        Index("idx_generation_tasks_batch_id", "batch_id"),
        Index("idx_generation_tasks_created_at", "created_at"),
    )


class TTSAudioFile(Base):
    """TTS语音文件表"""
    __tablename__ = "tts_audio_files"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    project_id = Column(BigInteger, ForeignKey("video_projects.id", ondelete="CASCADE"), nullable=True, comment="项目ID")
    script_id = Column(BigInteger, ForeignKey("scripts.id", ondelete="SET NULL"), nullable=True, comment="脚本ID")
    task_id = Column(BigInteger, ForeignKey("generation_tasks.id", ondelete="SET NULL"), nullable=True, comment="生成任务ID")

    voice_id = Column(BigInteger, ForeignKey("voice_clones.id", ondelete="SET NULL"), nullable=True, comment="音色ID")
    text_content = Column(Text, nullable=False, comment="文本内容")
    voice_config = Column(JSON, nullable=True, comment="语音配置")

    audio_url = Column(String(500), nullable=False, comment="音频文件URL")
    audio_path = Column(String(500), nullable=True, comment="音频存储路径")
    file_size = Column(BigInteger, nullable=True, comment="文件大小(字节)")
    duration = Column(DECIMAL(8, 2), nullable=True, comment="时长(秒)")
    format = Column(String(10), nullable=True, comment="格式")
    sample_rate = Column(BigInteger, nullable=True, comment="采样率")

    tts_provider = Column(String(50), nullable=True, comment="TTS提供商")
    tts_model = Column(String(100), nullable=True, comment="TTS模型")
    cost_cents = Column(BigInteger, nullable=True, comment="成本(分)")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_tts_audio_files_user_id", "user_id"),
        Index("idx_tts_audio_files_project_id", "project_id"),
        Index("idx_tts_audio_files_voice_id", "voice_id"),
    )