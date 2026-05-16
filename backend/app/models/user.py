"""
用户相关模型
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Enum, JSON, Index, Boolean
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    phone = Column(String(20), unique=True, nullable=True, comment="手机号")
    email = Column(String(100), unique=True, nullable=True, comment="邮箱")
    password_hash = Column(String(255), nullable=True, comment="密码哈希（手机注册用户可为空）")
    nickname = Column(String(50), nullable=False, comment="昵称")
    avatar_url = Column(String(500), nullable=True, comment="头像URL")
    bio = Column(Text, nullable=True, comment="个人简介")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    id_card_number = Column(String(18), nullable=True, comment="身份证号")
    real_name_verified = Column(Boolean, default=False, comment="实名认证状态")

    membership_type = Column(Enum("free", "basic", "pro", "enterprise"), default="free", comment="会员类型")
    membership_expire_at = Column(DateTime, nullable=True, comment="会员到期时间")

    quota_digital_human = Column(BigInteger, default=3, comment="数字人配额")
    quota_video_monthly = Column(BigInteger, default=10, comment="每月视频生成次数配额")
    quota_video_max_duration = Column(BigInteger, default=60, comment="单视频最长时长(秒)")
    quota_storage_mb = Column(BigInteger, default=1024, comment="存储空间配额(MB)")

    status = Column(Enum("active", "suspended", "deleted"), default="active", comment="账号状态")

    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")
    last_login_ip = Column(String(45), nullable=True, comment="最后登录IP")
    register_ip = Column(String(45), nullable=True, comment="注册IP")
    register_source = Column(Enum("web", "mobile", "wechat", "google", "apple"), default="web", comment="注册来源")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True, comment="软删除时间")

    __table_args__ = (
        Index("idx_users_phone", "phone"),
        Index("idx_users_email", "email"),
        Index("idx_users_membership", "membership_type", "membership_expire_at"),
        Index("idx_users_status", "status"),
        Index("idx_users_created_at", "created_at"),
    )


class UserLoginHistory(Base):
    """用户登录历史表"""
    __tablename__ = "user_login_histories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    login_type = Column(Enum("password", "sms", "oauth", "wechat", "google", "apple"), nullable=True, comment="登录方式")
    device_type = Column(Enum("web", "ios", "android", "unknown"), nullable=True, comment="设备类型")
    device_id = Column(String(100), nullable=True, comment="设备唯一标识")
    ip_address = Column(String(45), nullable=False, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="User-Agent信息")
    location_country = Column(String(50), nullable=True, comment="国家")
    location_province = Column(String(50), nullable=True, comment="省份")
    location_city = Column(String(50), nullable=True, comment="城市")
    is_abnormal = Column(Boolean, default=False, comment="是否异常登录")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_login_histories_user_id", "user_id"),
        Index("idx_ip", "ip_address"),
        Index("idx_user_login_histories_created_at", "created_at"),
    )


class UserDevice(Base):
    """用户绑定设备表"""
    __tablename__ = "user_devices"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    device_id = Column(String(100), nullable=False, comment="设备唯一标识")
    device_name = Column(String(100), nullable=True, comment="设备名称")
    device_type = Column(Enum("web", "ios", "android", "desktop"), nullable=True, comment="设备类型")
    os_version = Column(String(50), nullable=True, comment="系统版本")
    app_version = Column(String(50), nullable=True, comment="App版本")
    last_active_at = Column(DateTime, nullable=True, comment="最后活跃时间")
    is_active = Column(Boolean, default=True, comment="是否活跃")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_user_devices_user_id", "user_id"),
    )


class UserOAuthBinding(Base):
    """OAuth绑定表"""
    __tablename__ = "user_oauth_bindings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    provider = Column(Enum("wechat", "google", "apple"), nullable=False, comment="OAuth提供商")
    provider_user_id = Column(String(100), nullable=False, comment="第三方平台用户ID")
    access_token = Column(String(500), nullable=True, comment="访问令牌")
    refresh_token = Column(String(500), nullable=True, comment="刷新令牌")
    token_expire_at = Column(DateTime, nullable=True, comment="令牌过期时间")
    union_id = Column(String(100), nullable=True, comment="开放平台统一ID")
    avatar_url = Column(String(500), nullable=True, comment="第三方头像")
    nickname = Column(String(50), nullable=True, comment="第三方昵称")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_user_oauth_bindings_user_id", "user_id"),
    )