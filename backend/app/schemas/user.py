"""
用户相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuotaDetail(BaseModel):
    """配额详情"""
    total: int
    used: int
    remaining: int
    reset_at: Optional[datetime] = None


class QuotaInfo(BaseModel):
    """配额信息"""
    digital_human: QuotaDetail
    video_monthly: QuotaDetail
    video_max_duration: int
    storage_mb: QuotaDetail


class WalletInfo(BaseModel):
    """钱包信息"""
    balance: str = "0.00"
    frozen_balance: str = "0.00"


class UserProfileResponse(BaseModel):
    """用户资料响应"""
    id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    nickname: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    real_name: Optional[str] = None
    real_name_verified: bool = False
    membership_type: str
    membership_expire_at: Optional[datetime] = None
    quota: QuotaInfo
    wallet: WalletInfo
    created_at: datetime
    last_login_at: Optional[datetime] = None


class UpdateProfileRequest(BaseModel):
    """更新资料请求"""
    nickname: Optional[str] = Field(None, max_length=50)
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)


class DeviceInfo(BaseModel):
    """设备信息"""
    id: int
    device_name: Optional[str] = None
    device_type: str
    os_version: Optional[str] = None
    last_active_at: Optional[datetime] = None
    is_current: bool = False


class OAuthBindingInfo(BaseModel):
    """OAuth绑定信息"""
    id: int
    provider: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    binded_at: datetime