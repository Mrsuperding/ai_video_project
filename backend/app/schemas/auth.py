"""
认证相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SendSmsCodeRequest(BaseModel):
    """发送短信验证码请求"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$", description="手机号")
    code_type: str = Field(..., description="验证码类型: register/login/reset_password/bind_phone/unbind_phone")
    device_id: Optional[str] = Field(None, description="设备ID")
    ip_address: Optional[str] = Field(None, description="IP地址")


class SendSmsCodeResponse(BaseModel):
    """发送短信验证码响应"""
    expire_seconds: int = Field(..., description="过期秒数")
    retry_after: int = Field(..., description="重试间隔秒数")


class SmsLoginRequest(BaseModel):
    """短信验证码登录请求"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$", description="手机号")
    code: str = Field(..., min_length=4, max_length=10, description="验证码")
    device_id: Optional[str] = Field(None, description="设备ID")
    device_type: Optional[str] = Field("web", description="设备类型")


class PasswordLoginRequest(BaseModel):
    """密码登录请求"""
    account: str = Field(..., description="账号(手机号或邮箱)")
    password: str = Field(..., min_length=6, description="密码")
    device_id: Optional[str] = Field(None, description="设备ID")
    device_type: Optional[str] = Field("web", description="设备类型")


class OAuthLoginRequest(BaseModel):
    """OAuth登录请求"""
    provider: str = Field(..., description="提供商: wechat/google/apple")
    code: str = Field(..., description="授权码")
    state: Optional[str] = Field(None, description="随机状态")
    device_id: Optional[str] = Field(None, description="设备ID")
    device_type: Optional[str] = Field("mobile", description="设备类型")


class RefreshTokenRequest(BaseModel):
    """刷新Token请求"""
    refresh_token: str = Field(..., description="刷新令牌")


class TokenData(BaseModel):
    """Token数据"""
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"


class UserQuota(BaseModel):
    """用户配额"""
    digital_human: int
    video_monthly: int
    video_max_duration: int
    storage_mb: int


class UserInfo(BaseModel):
    """用户信息"""
    id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    nickname: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    membership_type: str = "free"
    membership_expire_at: Optional[datetime] = None
    quota: Optional[UserQuota] = None
    created_at: datetime


class LoginResponse(BaseModel):
    """登录响应"""
    user: UserInfo
    tokens: TokenData
    is_new_user: bool = False


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")


class ResetPasswordRequest(BaseModel):
    """重置密码请求"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    code: str = Field(..., description="验证码")
    new_password: str = Field(..., min_length=6)


class BindPhoneRequest(BaseModel):
    """绑定手机请求"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    code: str = Field(..., description="验证码")


class UnbindPhoneRequest(BaseModel):
    """解绑手机请求"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    password: str = Field(..., description="密码")


class BindEmailRequest(BaseModel):
    """绑定邮箱请求"""
    email: str = Field(..., format="email")
    code: str = Field(..., description="验证码")


class RealNameVerifyRequest(BaseModel):
    """实名认证请求"""
    real_name: str = Field(..., min_length=2, max_length=50)
    id_card_number: str = Field(..., pattern=r"^\d{17}[\dXx]$")
    id_card_front_url: str = Field(..., description="身份证正面图URL")
    id_card_back_url: str = Field(..., description="身份证背面图URL")