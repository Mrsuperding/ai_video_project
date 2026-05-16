"""
素材相关模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, JSON, Text, Index
from sqlalchemy.sql import func
from app.database import Base


class UserAsset(Base):
    """用户素材表"""
    __tablename__ = "user_assets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")

    asset_type = Column(Enum("image", "video", "audio", "font", "subtitle_style"), nullable=False, comment="素材类型")
    original_filename = Column(String(255), nullable=False, comment="原始文件名")
    file_url = Column(String(500), nullable=False, comment="文件URL")
    file_path = Column(String(500), nullable=True, comment="文件存储路径")
    file_size = Column(BigInteger, nullable=False, comment="文件大小(字节)")

    width = Column(BigInteger, nullable=True, comment="宽度")
    height = Column(BigInteger, nullable=True, comment="高度")
    duration = Column(Text, nullable=True, comment="时长")
    fps = Column(Text, nullable=True, comment="帧率")
    audio_channels = Column(BigInteger, nullable=True, comment="声道数")
    codec = Column(String(50), nullable=True, comment="编码格式")

    name = Column(String(200), nullable=False, comment="素材名称")
    description = Column(Text, nullable=True, comment="描述")
    category = Column(String(50), nullable=True, comment="分类")
    tags = Column(JSON, nullable=True, comment="标签")
    color = Column(String(20), nullable=True, comment="主色调")

    usage_count = Column(BigInteger, default=0, comment="使用次数")

    status = Column(Enum("uploading", "processing", "ready", "failed"), default="uploading", comment="状态")
    error_message = Column(Text, nullable=True, comment="错误信息")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True, comment="软删除时间")

    __table_args__ = (
        Index("idx_user_assets_user_id", "user_id"),
        Index("idx_user_assets_asset_type", "asset_type"),
        Index("idx_user_assets_category", "category"),
        Index("idx_user_assets_status", "status"),
        Index("idx_user_assets_created_at", "created_at"),
    )


class PlatformAsset(Base):
    """平台素材库表"""
    __tablename__ = "platform_assets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    asset_type = Column(Enum("background", "bgm", "transition", "sticker", "subtitle_style", "particle_effect"), nullable=False, comment="素材类型")
    original_filename = Column(String(255), nullable=False, comment="原始文件名")
    file_url = Column(String(500), nullable=False, comment="文件URL")
    file_path = Column(String(500), nullable=True, comment="文件存储路径")
    file_size = Column(BigInteger, nullable=True, comment="文件大小(字节)")

    width = Column(BigInteger, nullable=True, comment="宽度")
    height = Column(BigInteger, nullable=True, comment="高度")
    duration = Column(Text, nullable=True, comment="时长")
    fps = Column(Text, nullable=True, comment="帧率")

    category = Column(String(50), nullable=False, comment="分类")
    subcategory = Column(String(50), nullable=True, comment="子分类")
    tags = Column(JSON, nullable=True, comment="标签")

    license_type = Column(Enum("free", "premium", "exclusive"), nullable=True, comment="授权类型")
    membership_required = Column(Enum("free", "all", "basic", "pro", "enterprise"), default="free", comment="会员等级要求")

    usage_count = Column(BigInteger, default=0, comment="使用次数")
    view_count = Column(BigInteger, default=0, comment="查看次数")

    status = Column(Enum("active", "inactive", "deleted"), default="active", comment="状态")

    uploader_id = Column(BigInteger, nullable=True, comment="上传者ID")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_platform_assets_asset_type", "asset_type"),
        Index("idx_platform_assets_category", "category"),
        Index("idx_license", "license_type", "membership_required"),
        Index("idx_platform_assets_status", "status"),
        Index("idx_platform_assets_usage_count", "usage_count"),
    )


class AssetCategory(Base):
    """素材分类表"""
    __tablename__ = "asset_categories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="分类名称")
    name_en = Column(String(100), nullable=True, comment="英文名称")
    icon = Column(String(100), nullable=True, comment="图标")

    parent_id = Column(BigInteger, nullable=True, comment="父分类ID")
    level = Column(BigInteger, default=1, comment="层级")
    path = Column(String(200), nullable=True, comment="路径串")

    asset_types = Column(JSON, nullable=True, comment="适用素材类型")

    sort_order = Column(BigInteger, default=0, comment="排序序号")

    status = Column(Enum("active", "inactive"), default="active")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_asset_categories_parent_id", "parent_id"),
        Index("idx_asset_categories_level", "level"),
        Index("idx_asset_categories_status", "status"),
    )