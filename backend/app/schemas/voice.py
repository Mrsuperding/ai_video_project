"""
声音克隆相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VoiceCloneItem(BaseModel):
    """声音克隆列表项"""
    id: int
    name: str
    gender: Optional[str] = None
    age_group: Optional[str] = None
    status: str
    sample_audio_url: Optional[str] = None
    duration: Optional[float] = None
    usage_count: int = 0
    is_default: bool = False
    created_at: datetime


class CreateVoiceCloneRequest(BaseModel):
    """创建声音克隆请求"""
    name: str = Field(..., max_length=100)
    source_audio_url: str
    language: Optional[str] = "zh"
    emotion: Optional[str] = "neutral"


class CreateVoiceCloneResponse(BaseModel):
    """创建声音克隆响应"""
    id: int
    status: str
    task_id: int
    estimated_seconds: int = 300