"""
脚本相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ScriptSegment(BaseModel):
    """脚本段落"""
    id: Optional[int] = None
    text: str
    duration: Optional[float] = None
    speed: float = 1.0
    pause_after: float = 0.5
    emotion: str = "neutral"


class ScriptContent(BaseModel):
    """脚本内容"""
    segments: List[ScriptSegment]


class ScriptItem(BaseModel):
    """脚本列表项"""
    id: int
    title: str
    description: Optional[str] = None
    word_count: Optional[int] = None
    estimated_duration: Optional[float] = None
    language: str = "zh"
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    status: str
    usage_count: int = 0
    created_at: datetime


class ScriptDetail(BaseModel):
    """脚本详情"""
    id: int
    title: str
    description: Optional[str] = None
    content: ScriptContent
    word_count: Optional[int] = None
    estimated_duration: Optional[float] = None
    language: str
    voice_id: Optional[int] = None
    base_tts_speed: float = 1.0
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    status: str
    created_at: datetime
    updated_at: datetime


class CreateScriptRequest(BaseModel):
    """创建脚本请求"""
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    language: Optional[str] = "zh"
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class UpdateScriptRequest(BaseModel):
    """更新脚本请求"""
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[ScriptContent] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class SaveAsTemplateRequest(BaseModel):
    """保存为模板请求"""
    name: str
    description: Optional[str] = None
    category: Optional[str] = None


class AIGenerateRequest(BaseModel):
    """AI生成请求"""
    input_type: str = Field(..., description="template/prompt")
    template_id: Optional[int] = None
    template_params: Optional[Dict[str, Any]] = None
    input_prompt: Optional[str] = None
    style: Optional[str] = "professional"
    emotion: Optional[str] = "neutral"
    target_language: str = "zh"
    duration_seconds: Optional[int] = 60


class AIRewriteRequest(BaseModel):
    """AI改写请求"""
    text: str
    task_type: str = Field(..., description="rewrite/polish/expand/shrink/translate")
    style: Optional[str] = "professional"
    target_language: Optional[str] = "zh"


class AIWritingTaskResponse(BaseModel):
    """AI写作任务响应"""
    id: int
    task_type: str
    status: str
    progress: int
    result: Optional[Dict[str, Any]] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cost_cents: Optional[int] = None


class ScriptTemplateItem(BaseModel):
    """脚本模板列表项"""
    id: int
    name: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    category: str
    tags: Optional[List[str]] = None
    input_fields: Optional[List[Dict]] = None
    usage_count: int = 0
    rating: Optional[float] = None
    created_at: datetime


class ScriptTemplateDetail(BaseModel):
    """脚本模板详情"""
    id: int
    name: str
    description: Optional[str] = None
    prompt_template: Optional[str] = None
    example_text: Optional[str] = None
    category: str
    input_fields: List[Dict]
    usage_count: int = 0
    rating: Optional[float] = None
    rating_count: int = 0