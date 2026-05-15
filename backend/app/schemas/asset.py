"""
素材相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class UserAssetItem(BaseModel):
    """用户素材列表项"""
    id: int
    name: str
    asset_type: str
    file_url: str
    thumbnail_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    file_size: int
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    usage_count: int = 0
    created_at: datetime


class UploadTokenRequest(BaseModel):
    """获取上传凭证请求"""
    file_name: str
    file_size: int
    asset_type: str


class UploadTokenResponse(BaseModel):
    """上传凭证响应"""
    upload_url: str
    upload_token: str
    asset_id: int
    expire_seconds: int


class ConfirmUploadRequest(BaseModel):
    """确认上传请求"""
    name: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class UpdateAssetRequest(BaseModel):
    """更新素材请求"""
    name: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class PlatformAssetItem(BaseModel):
    """平台素材列表项"""
    id: int
    asset_type: str
    file_url: str
    thumbnail_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    category: str
    license_type: str
    membership_required: str
    usage_count: int = 0


class AssetCategoryItem(BaseModel):
    """素材分类项"""
    id: int
    name: str
    subcategories: Optional[List["AssetCategoryItem"]] = None