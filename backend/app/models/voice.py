"""
声音克隆模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, Text, DECIMAL, Index, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base


class VoiceClone(Base):
    """声音克隆表"""
    __tablename__ = "voice_clones"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    digital_human_id = Column(BigInteger, ForeignKey("digital_humans.id", ondelete="SET NULL"), nullable=True, comment="关联数字人ID")
    name = Column(String(100), nullable=False, comment="音色名称")

    source_audio_url = Column(String(500), nullable=False, comment="源音频文件URL")
    source_duration = Column(DECIMAL(6, 2), nullable=True, comment="源音频时长(秒)")
    language = Column(String(10), nullable=True, comment="语言")

    status = Column(Enum("pending", "processing", "completed", "failed"), default="pending", comment="生成状态")
    model_provider = Column(String(50), nullable=True, comment="TTS提供商")
    model_name = Column(String(100), nullable=True, comment="TTS模型")

    voice_id = Column(String(100), nullable=True, comment="TTS平台返回的音色ID")
    sample_audio_url = Column(String(500), nullable=True, comment="示例音频URL")

    gender = Column(Enum("male", "female", "neutral"), nullable=True, comment="性别")
    age_group = Column(Enum("young", "middle", "senior"), nullable=True, comment="年龄段")
    emotion = Column(Enum("neutral", "happy", "sad", "angry"), nullable=True, comment="情感倾向")

    usage_count = Column(BigInteger, default=0, comment="使用次数")
    is_default = Column(Boolean, default=False, comment="是否为默认音色")

    error_message = Column(Text, nullable=True, comment="错误信息")
    retry_count = Column(BigInteger, default=0, comment="重试次数")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_voice_clones_user_id", "user_id"),
        Index("idx_voice_clones_idx_digital_human_id", "digital_human_id"),
        Index("idx_voice_clones_status", "status"),
    )