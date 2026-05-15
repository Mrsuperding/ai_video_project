"""
管理后台相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AdminLoginRequest(BaseModel):
    """管理员登录请求"""
    username: str
    password: str


class AdminInfo(BaseModel):
    """管理员信息"""
    id: int
    username: str
    real_name: str
    role: str


class AdminLoginResponse(BaseModel):
    """管理员登录响应"""
    admin: AdminInfo
    tokens: dict


class AdminUserItem(BaseModel):
    """管理员用户列表项"""
    id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    nickname: str
    avatar_url: Optional[str] = None
    membership_type: str
    status: str
    balance: str
    created_at: datetime
    last_login_at: Optional[datetime] = None


class AdminUserDetail(BaseModel):
    """管理员用户详情"""
    id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    nickname: str
    avatar_url: Optional[str] = None
    real_name: Optional[str] = None
    id_card_number: Optional[str] = None
    real_name_verified: bool
    membership_type: str
    membership_expire_at: Optional[datetime] = None
    status: str
    balance: str
    frozen_balance: str
    quota: dict
    register_ip: Optional[str] = None
    register_source: str
    created_at: datetime
    last_login_at: Optional[datetime] = None
    last_login_ip: Optional[str] = None


class BanUserRequest(BaseModel):
    """封禁用户请求"""
    action: str = Field(..., description="ban/unban")
    reason: Optional[str] = None


class ReviewItem(BaseModel):
    """审核项"""
    id: int
    user_id: int
    target_type: str
    target_id: int
    review_type: str
    risk_score: Optional[float] = None
    risk_labels: Optional[List[str]] = None
    submit_data: Optional[Dict] = None
    created_at: datetime


class ApproveReviewRequest(BaseModel):
    """审核通过请求"""
    note: Optional[str] = None


class RejectReviewRequest(BaseModel):
    """审核驳回请求"""
    reason: str
    note: Optional[str] = None


class PlatformStatisticsResponse(BaseModel):
    """平台统计响应"""
    period: str
    start_date: str
    end_date: str
    users: Dict[str, Any]
    business: Dict[str, Any]
    finance: Dict[str, Any]
    models: Optional[Dict[str, Any]] = None


class SystemConfigItem(BaseModel):
    """系统配置项"""
    key: str
    value: str
    type: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_editable: bool = True


class UpdateConfigsRequest(BaseModel):
    """更新配置请求"""
    configs: List[Dict[str, str]]


class WebhookRequest(BaseModel):
    """Webhook配置请求"""
    url: str
    events: List[str]
    secret: str


class WebhookResponse(BaseModel):
    """Webhook响应"""
    id: int
    url: str
    events: List[str]
    secret: str
    status: str