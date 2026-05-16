"""
扩展模型 - 缺失的数据表
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, Text, JSON, Index, Boolean, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from app.database import Base


class DigitalHumanPhoto(Base):
    """数字人照片表"""
    __tablename__ = "digital_human_photos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    digital_human_id = Column(BigInteger, ForeignKey("digital_humans.id", ondelete="CASCADE"), nullable=False, comment="数字人ID")
    user_id = Column(BigInteger, nullable=False, comment="用户ID")

    photo_url = Column(String(500), nullable=False, comment="照片URL")
    photo_type = Column(Enum("source", "processed", "preview", "result"), default="source", comment="照片类型")
    photo_order = Column(BigInteger, default=0, comment="照片顺序")
    file_size = Column(BigInteger, nullable=True, comment="文件大小(字节)")
    width = Column(BigInteger, nullable=True, comment="宽度")
    height = Column(BigInteger, nullable=True, comment="高度")

    is_checked = Column(Boolean, default=False, comment="是否审核通过")
    check_result = Column(Enum("pending", "approved", "rejected"), default="pending", comment="审核结果")
    check_reason = Column(String(255), nullable=True, comment="审核原因")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_digital_human_photos_digital_human_id", "digital_human_id"),
        Index("idx_digital_human_photos_user_id", "user_id"),
        Index("idx_digital_human_photos_photo_type", "photo_type"),
    )


class AuthorizationProof(Base):
    """授权证明表"""
    __tablename__ = "authorization_proofs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    digital_human_id = Column(BigInteger, ForeignKey("digital_humans.id", ondelete="CASCADE"), nullable=False, comment="数字人ID")
    user_id = Column(BigInteger, nullable=False, comment="用户ID")

    proof_type = Column(Enum("id_card", "company_cert", "authorization_letter", "other"), nullable=False, comment="证明类型")
    proof_url = Column(String(500), nullable=False, comment="证明文件URL")
    proof_number = Column(String(100), nullable=True, comment="证明编号(身份证号/营业执照号等)")
    holder_name = Column(String(100), nullable=True, comment="持证人姓名")
    holder_id_card = Column(String(18), nullable=True, comment="持证人身份证号")

    status = Column(Enum("pending", "approved", "rejected"), default="pending", comment="审核状态")
    reviewer_id = Column(BigInteger, nullable=True, comment="审核员ID")
    review_comment = Column(String(500), nullable=True, comment="审核备注")
    reviewed_at = Column(DateTime, nullable=True, comment="审核时间")

    expire_at = Column(DateTime, nullable=True, comment="过期时间")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_authorization_proofs_digital_human_id", "digital_human_id"),
        Index("idx_authorization_proofs_user_id", "user_id"),
        Index("idx_authorization_proofs_status", "status"),
    )


class VoicePreset(Base):
    """声音预设表"""
    __tablename__ = "voice_presets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=True, comment="用户ID(Null表示公共预设)")
    name = Column(String(100), nullable=False, comment="预设名称")

    language = Column(String(10), nullable=True, comment="语言")
    gender = Column(Enum("male", "female", "neutral"), nullable=True, comment="性别")
    age_group = Column(Enum("child", "young", "middle", "senior"), nullable=True, comment="年龄段")
    emotion = Column(Enum("neutral", "happy", "sad", "angry", "formal", "casual"), default="neutral", comment="情感")

    speed = Column(DECIMAL(3, 2), default=1.00, comment="语速")
    pitch = Column(DECIMAL(3, 2), default=1.00, comment="音调")
    volume = Column(DECIMAL(3, 2), default=1.00, comment="音量")

    provider = Column(String(50), nullable=True, comment="TTS提供商")
    provider_voice_id = Column(String(100), nullable=True, comment="提供商音色ID")

    usage_count = Column(BigInteger, default=0, comment="使用次数")
    is_public = Column(Boolean, default=False, comment="是否公开")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_voice_presets_user_id", "user_id"),
        Index("idx_voice_presets_language", "language"),
        Index("idx_voice_presets_is_public", "is_public"),
    )


class TTSCache(Base):
    """TTS缓存表"""
    __tablename__ = "tts_cache"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")

    text_hash = Column(String(64), nullable=False, comment="文本哈希")
    text_content = Column(Text, nullable=False, comment="文本内容")
    voice_id = Column(BigInteger, ForeignKey("voice_clones.id", ondelete="CASCADE"), nullable=False, comment="音色ID")
    voice_config = Column(JSON, nullable=True, comment="语音配置")

    audio_url = Column(String(500), nullable=False, comment="音频URL")
    audio_path = Column(String(500), nullable=True, comment="音频存储路径")
    file_size = Column(BigInteger, nullable=True, comment="文件大小(字节)")
    duration = Column(DECIMAL(8, 2), nullable=True, comment="时长(秒)")

    provider = Column(String(50), nullable=True, comment="TTS提供商")
    cost_cents = Column(BigInteger, nullable=True, comment="成本(分)")

    hit_count = Column(BigInteger, default=0, comment="命中次数")
    last_hit_at = Column(DateTime, nullable=True, comment="最后命中时间")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_tts_cache_text_hash", "text_hash"),
        Index("idx_tts_cache_voice_id", "voice_id"),
        Index("idx_tts_cache_user_id", "user_id"),
    )


class ShareAccessLog(Base):
    """分享访问日志表"""
    __tablename__ = "share_access_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    share_token = Column(String(100), nullable=False, comment="分享Token")
    video_output_id = Column(BigInteger, ForeignKey("video_outputs.id", ondelete="CASCADE"), nullable=False, comment="视频输出ID")

    visitor_ip = Column(String(45), nullable=True, comment="访问者IP")
    visitor_country = Column(String(50), nullable=True, comment="国家")
    visitor_province = Column(String(50), nullable=True, comment="省份")
    visitor_city = Column(String(50), nullable=True, comment="城市")
    device_type = Column(Enum("web", "ios", "android", "other"), nullable=True, comment="设备类型")
    user_agent = Column(Text, nullable=True, comment="User-Agent")

    access_count = Column(BigInteger, default=1, comment="访问次数(同一IP/设备累加)")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_share_access_logs_share_token", "share_token"),
        Index("idx_share_access_logs_video_output_id", "video_output_id"),
        Index("idx_share_access_logs_created_at", "created_at"),
    )


class PaymentOrder(Base):
    """支付订单表"""
    __tablename__ = "payment_orders"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_no = Column(String(50), nullable=False, unique=True, comment="订单号")
    user_id = Column(BigInteger, nullable=False, comment="用户ID")

    order_type = Column(Enum("membership", "recharge", "asset", "other"), nullable=False, comment="订单类型")
    product_id = Column(BigInteger, nullable=True, comment="商品ID")
    product_name = Column(String(200), nullable=True, comment="商品名称")

    original_amount = Column(DECIMAL(10, 2), nullable=False, comment="原价")
    discount_amount = Column(DECIMAL(10, 2), default=0.00, comment="优惠金额")
    actual_amount = Column(DECIMAL(10, 2), nullable=False, comment="实付金额")

    payment_method = Column(Enum("alipay", "wechat", "stripe", "wallet", "coupon"), nullable=True, comment="支付方式")
    payment_status = Column(Enum("pending", "paid", "cancelled", "refunded", "failed"), default="pending", comment="支付状态")
    payment_time = Column(DateTime, nullable=True, comment="支付时间")

    coupon_id = Column(BigInteger, ForeignKey("coupons.id", ondelete="SET NULL"), nullable=True, comment="使用的优惠券ID")
    coupon_code = Column(String(50), nullable=True, comment="优惠券码")

    trade_no = Column(String(100), nullable=True, comment="第三方交易号")
    callback_data = Column(JSON, nullable=True, comment="回调数据")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_payment_orders_user_id", "user_id"),
        Index("idx_payment_orders_order_no", "order_no"),
        Index("idx_payment_orders_payment_status", "payment_status"),
        Index("idx_payment_orders_created_at", "created_at"),
    )


class ConsumptionRecord(Base):
    """消费记录表"""
    __tablename__ = "consumption_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    order_no = Column(String(50), nullable=True, comment="关联订单号")

    consumption_type = Column(Enum("video_gen", "tts", "digital_human", "storage", "api_call", "other"), nullable=False, comment="消费类型")
    resource_id = Column(BigInteger, nullable=True, comment="资源ID(如视频项目ID)")
    resource_name = Column(String(200), nullable=True, comment="资源名称")

    quantity = Column(BigInteger, default=1, comment="数量")
    unit_price = Column(DECIMAL(10, 4), nullable=False, comment="单价")
    total_amount = Column(DECIMAL(10, 2), nullable=False, comment="总金额")

    before_balance = Column(DECIMAL(10, 2), nullable=False, comment="消费前余额")
    after_balance = Column(DECIMAL(10, 2), nullable=False, comment="消费后余额")

    provider = Column(String(50), nullable=True, comment="服务提供商")
    model_name = Column(String(100), nullable=True, comment="模型名称")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_consumption_records_user_id", "user_id"),
        Index("idx_consumption_records_consumption_type", "consumption_type"),
        Index("idx_consumption_records_created_at", "created_at"),
    )


class MembershipPlan(Base):
    """会员计划表"""
    __tablename__ = "membership_plans"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    plan_type = Column(Enum("free", "basic", "pro", "enterprise"), nullable=False, unique=True, comment="计划类型")
    plan_name = Column(String(50), nullable=False, comment="计划名称")

    price = Column(DECIMAL(10, 2), nullable=False, comment="价格(月)")
    annual_price = Column(DECIMAL(10, 2), nullable=True, comment="年付价格")
    discount_percent = Column(BigInteger, nullable=True, comment="年付折扣百分比")

    quota_digital_human = Column(BigInteger, default=3, comment="数字人配额")
    quota_video_monthly = Column(BigInteger, default=10, comment="每月视频生成次数配额")
    quota_video_max_duration = Column(BigInteger, default=60, comment="单视频最长时长(秒)")
    quota_storage_mb = Column(BigInteger, default=1024, comment="存储空间配额(MB)")
    quota_api_calls = Column(BigInteger, nullable=True, comment="API调用配额(每月)")

    features = Column(JSON, nullable=True, comment="功能列表")

    sort_order = Column(BigInteger, default=0, comment="排序顺序")
    is_active = Column(Boolean, default=True, comment="是否启用")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_membership_plans_plan_type", "plan_type"),
        Index("idx_membership_plans_is_active", "is_active"),
    )


class UserViolation(Base):
    """用户违规表"""
    __tablename__ = "user_violations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")

    violation_type = Column(Enum("content_violation", "spam", "abuse", "fraud", "other"), nullable=False, comment="违规类型")
    violation_level = Column(Enum("warning", "minor", "major", "critical"), default="warning", comment="违规等级")

    target_type = Column(String(50), nullable=True, comment="违规对象类型")
    target_id = Column(BigInteger, nullable=True, comment="违规对象ID")
    target_content = Column(Text, nullable=True, comment="违规内容")

    description = Column(Text, nullable=True, comment="违规描述")
    evidence_urls = Column(JSON, nullable=True, comment="证据截图URLs")

    handler_id = Column(BigInteger, nullable=True, comment="处理员ID")
    handle_result = Column(Enum("warning", "delete_content", "disable_user", "ban_user"), nullable=False, comment="处理结果")
    handle_comment = Column(String(500), nullable=True, comment="处理备注")

    status = Column(Enum("pending", "handled", "appealed", "cleared"), default="pending", comment="状态")
    appealed_at = Column(DateTime, nullable=True, comment="申诉时间")
    appeal_result = Column(String(255), nullable=True, comment="申诉结果")
    cleared_at = Column(DateTime, nullable=True, comment="解除时间")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_user_violations_user_id", "user_id"),
        Index("idx_user_violations_violation_type", "violation_type"),
        Index("idx_user_violations_status", "status"),
        Index("idx_user_violations_created_at", "created_at"),
    )


class SensitiveWord(Base):
    """敏感词表"""
    __tablename__ = "sensitive_words"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    word = Column(String(100), nullable=False, unique=True, comment="敏感词")
    word_type = Column(Enum("politics", "porn", "violence", "crime", "custom"), nullable=False, comment="敏感词类型")

    severity_level = Column(BigInteger, default=1, comment="严重程度(1-5)")
    replacement = Column(String(50), nullable=True, comment="替换词")

    is_active = Column(Boolean, default=True, comment="是否启用")

    created_by = Column(BigInteger, nullable=True, comment="创建人ID")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_sensitive_words_word_type", "word_type"),
        Index("idx_sensitive_words_is_active", "is_active"),
        Index("idx_sensitive_words_severity_level", "severity_level"),
    )