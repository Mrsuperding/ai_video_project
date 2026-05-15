"""
视频相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DigitalHumanSummary(BaseModel):
    """数字人摘要"""
    id: int
    name: str
    preview_image_url: Optional[str] = None


class ScriptSummary(BaseModel):
    """脚本摘要"""
    id: int
    title: str


class VideoProjectItem(BaseModel):
    """视频项目列表项"""
    id: int
    project_name: str
    description: Optional[str] = None
    status: str
    resolution: str
    aspect_ratio: str
    duration: Optional[float] = None
    thumbnail_url: Optional[str] = None
    digital_human: Optional[DigitalHumanSummary] = None
    script: Optional[ScriptSummary] = None
    view_count: int = 0
    download_count: int = 0
    created_at: datetime
    updated_at: datetime
    progress: Optional[int] = None
    estimated_remaining_seconds: Optional[int] = None


class VideoOutputInfo(BaseModel):
    """视频输出信息"""
    id: int
    video_url: str
    thumbnail_url: Optional[str] = None
    video_file_size: Optional[int] = None
    resolution: str
    duration: Optional[float] = None
    fps: Optional[int] = None
    codec: Optional[str] = None
    bitrate: Optional[int] = None
    has_audio: bool = True
    quality_score: Optional[int] = None
    review_status: str
    watermark_embedded: bool = False
    view_count: int = 0
    download_count: int = 0
    share_count: int = 0
    created_at: datetime


class VideoProjectDetail(BaseModel):
    """视频项目详情"""
    id: int
    user_id: int
    project_name: str
    description: Optional[str] = None
    resolution: str
    aspect_ratio: str
    fps: int
    max_duration: Optional[int] = None
    generation_status: str
    priority: int = 5
    digital_human_id: int
    digital_human_config: Optional[Dict] = None
    script_id: int
    script_content: Optional[Dict] = None
    voice_id: Optional[int] = None
    tts_config: Optional[Dict] = None
    background_asset_id: Optional[int] = None
    background_type: str
    background_value: Optional[str] = None
    bgm_asset_id: Optional[int] = None
    bgm_volume: float = 0.3
    subtitle_config: Optional[Dict] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    view_count: int = 0
    download_count: int = 0
    share_count: int = 0
    cost_cents: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    output: Optional[VideoOutputInfo] = None


class CreateVideoProjectRequest(BaseModel):
    """创建视频项目请求"""
    project_name: str = Field(..., max_length=200)
    description: Optional[str] = None
    mode: str = "simple"
    resolution: Optional[str] = "1080p"
    aspect_ratio: Optional[str] = "16:9"
    fps: Optional[int] = 30
    digital_human_id: int
    digital_human_config: Optional[Dict] = None
    script_id: int
    voice_id: Optional[int] = None
    tts_config: Optional[Dict] = None
    background_asset_id: Optional[int] = None
    background_type: Optional[str] = "image"
    background_value: Optional[str] = None
    bgm_asset_id: Optional[int] = None
    bgm_volume: Optional[float] = 0.3
    timeline_config: Optional[Dict] = None
    subtitle_config: Optional[Dict] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None


class CreateProjectResponse(BaseModel):
    """创建项目响应"""
    id: int
    project_name: str
    status: str
    estimated_cost_cents: int


class GenerateRequest(BaseModel):
    """提交生成请求"""
    priority: Optional[int] = 5
    skip_queue: Optional[bool] = False


class GenerateResponse(BaseModel):
    """生成响应"""
    project_id: int
    task_id: int
    status: str
    queue_position: Optional[int] = None
    estimated_seconds: int


class GenerationTaskResponse(BaseModel):
    """生成任务响应"""
    id: int
    project_id: int
    project_name: Optional[str] = None
    task_type: str
    status: str
    progress: int
    current_step: Optional[str] = None
    model_provider: Optional[str] = None
    model_name: Optional[str] = None
    started_at: Optional[datetime] = None
    estimated_remaining_seconds: Optional[int] = None


class ShareVideoRequest(BaseModel):
    """分享视频请求"""
    expire_hours: Optional[int] = 24
    enable_password: Optional[bool] = False
    password: Optional[str] = None


class ShareVideoResponse(BaseModel):
    """分享视频响应"""
    share_url: str
    share_token: str
    expire_at: datetime
    has_password: bool


class UpdateProjectRequest(BaseModel):
    """更新项目请求"""
    project_name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class RegenerateProjectRequest(BaseModel):
    """重新生成项目请求"""
    keep_output: Optional[bool] = False
    config_changes: Optional[Dict] = None


class BatchOperationRequest(BaseModel):
    """批量操作请求"""
    action: str = Field(..., description="delete/archive/restore")
    project_ids: List[int]