"""
数字人相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SourcePhoto(BaseModel):
    """源照片"""
    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    face_count: Optional[int] = None


class DigitalHumanItem(BaseModel):
    """数字人列表项"""
    id: int
    name: str
    description: Optional[str] = None
    status: str
    preview_image_url: Optional[str] = None
    preview_video_url: Optional[str] = None
    preview_video_duration: Optional[float] = None
    usage_count: int = 0
    is_default: bool = False
    authorization_type: str
    authorization_status: Optional[str] = None
    created_at: datetime
    progress: Optional[int] = None
    estimated_remaining_seconds: Optional[int] = None


class DigitalHumanDetail(BaseModel):
    """数字人详情"""
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    source_type: str
    source_photos: Optional[List[SourcePhoto]] = None
    photo_count: Optional[int] = None
    gender: Optional[str] = None
    age_group: Optional[str] = None
    clothing_type: Optional[str] = None
    background_type: Optional[str] = None
    status: str
    preview_image_url: Optional[str] = None
    preview_video_url: Optional[str] = None
    usage_count: int = 0
    is_default: bool = False
    authorization_type: str
    authorization_status: str
    version_number: int = 1
    created_at: datetime
    updated_at: datetime


class CreateDigitalHumanRequest(BaseModel):
    """创建数字人请求"""
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    source_type: str = "single_photo"
    source_photos: List[SourcePhoto]
    authorization_type: str = Field(..., description="self/others/public")
    authorization_proof_url: Optional[str] = None
    authorization_expire_at: Optional[datetime] = None
    clothing_type: Optional[str] = None
    background_type: Optional[str] = None
    customize: Optional[Dict[str, Any]] = None


class CreateDigitalHumanResponse(BaseModel):
    """创建数字人响应"""
    id: int
    name: str
    status: str
    task_id: int
    estimated_seconds: int = 600


class UpdateDigitalHumanRequest(BaseModel):
    """更新数字人请求"""
    name: Optional[str] = None
    description: Optional[str] = None


class RegenerateRequest(BaseModel):
    """重新生成请求"""
    new_photos: List[SourcePhoto]


class DigitalHumanTaskResponse(BaseModel):
    """数字人任务响应"""
    id: int
    task_type: str
    status: str
    progress: int
    current_step: Optional[str] = None
    estimated_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    created_at: datetime


class UploadTokenResponse(BaseModel):
    """上传凭证响应"""
    upload_token: str
    upload_url: str
    expire_seconds: int
    file_prefix: str