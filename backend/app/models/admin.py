"""
管理后台相关模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, Text, JSON, Index, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Admin(Base):
    """管理员表"""
    __tablename__ = "admins"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    email = Column(String(100), nullable=True, unique=True, comment="邮箱")
    phone = Column(String(20), nullable=True, comment="手机号")
    avatar_url = Column(String(500), nullable=True, comment="头像")

    role = Column(Enum("super_admin", "admin", "content_reviewer", "operator", "viewer"), nullable=False, comment="角色")
    permissions = Column(JSON, nullable=True, comment="权限列表")

    status = Column(Enum("active", "suspended", "deleted"), default="active", comment="状态")

    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")
    last_login_ip = Column(String(45), nullable=True, comment="最后登录IP")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_admins_role", "role"),
        Index("idx_admins_status", "status"),
    )


class AdminOperationLog(Base):
    """管理员操作日志表"""
    __tablename__ = "admin_operation_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    admin_id = Column(BigInteger, nullable=False, comment="管理员ID")
    admin_name = Column(String(50), nullable=True, comment="管理员用户名")

    action = Column(String(100), nullable=False, comment="操作")
    module = Column(String(50), nullable=False, comment="模块")
    operation_type = Column(Enum("create", "update", "delete", "view", "approve", "reject", "other"), nullable=False, comment="操作类型")
    description = Column(Text, nullable=True, comment="操作描述")

    target_type = Column(String(50), nullable=True, comment="目标类型")
    target_id = Column(BigInteger, nullable=True, comment="目标ID")

    before_data = Column(JSON, nullable=True, comment="变更前数据")
    after_data = Column(JSON, nullable=True, comment="变更后数据")
    changed_fields = Column(JSON, nullable=True, comment="变更字段列表")

    request_method = Column(String(10), nullable=True, comment="请求方法")
    request_uri = Column(String(500), nullable=True, comment="请求URI")
    request_params = Column(Text, nullable=True, comment="请求参数")
    ip_address = Column(String(45), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="User-Agent")

    result = Column(Enum("success", "failed"), nullable=False, comment="结果")
    error_message = Column(Text, nullable=True, comment="错误信息")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_admin_operation_logs_admin_id", "admin_id"),
        Index("idx_admin_operation_logs_action", "action"),
        Index("idx_admin_operation_logs_target", "target_type", "target_id"),
        Index("idx_admin_operation_logs_created_at", "created_at"),
    )


class SystemConfig(Base):
    """系统配置表"""
    __tablename__ = "system_configs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    config_key = Column(String(100), nullable=False, unique=True, comment="配置键")
    config_value = Column(Text, nullable=False, comment="配置值")
    config_type = Column(Enum("string", "number", "boolean", "json"), default="string", comment="配置类型")
    description = Column(String(255), nullable=True, comment="描述")
    category = Column(String(50), nullable=True, comment="分类")

    is_public = Column(Boolean, default=False, comment="是否公开")
    is_editable = Column(Boolean, default=True, comment="是否可编辑")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_system_configs_category", "category"),
        Index("idx_system_configs_is_public", "is_public"),
    )