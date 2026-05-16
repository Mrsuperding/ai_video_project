"""
会员与优惠券模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, DECIMAL, JSON, Index, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class UserMembership(Base):
    """会员订阅表"""
    __tablename__ = "user_memberships"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    membership_type = Column(Enum("basic", "pro", "enterprise"), nullable=False, comment="会员类型")
    original_price = Column(DECIMAL(10, 2), nullable=True, comment="原价")
    actual_price = Column(DECIMAL(10, 2), nullable=False, comment="实付金额")
    payment_method = Column(Enum("alipay", "wechat", "stripe", "wallet", "coupon"), nullable=True, comment="支付方式")
    order_no = Column(String(50), nullable=False, unique=True, comment="订单号")

    start_at = Column(DateTime, nullable=False, comment="开始时间")
    end_at = Column(DateTime, nullable=False, comment="结束时间")
    auto_renew = Column(Boolean, default=False, comment="是否自动续费")

    coupon_id = Column(BigInteger, ForeignKey("coupons.id", ondelete="SET NULL"), nullable=True, comment="使用的优惠券ID")
    discount_amount = Column(DECIMAL(10, 2), default=0.00, comment="优惠金额")

    status = Column(Enum("pending", "paid", "cancelled", "expired", "refund"), default="pending", comment="订单状态")
    paid_at = Column(DateTime, nullable=True, comment="支付时间")
    refund_at = Column(DateTime, nullable=True, comment="退款时间")
    refund_amount = Column(DECIMAL(10, 2), nullable=True, comment="退款金额")
    refund_reason = Column(String(255), nullable=True, comment="退款原因")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_user_memberships_user_id", "user_id"),
        Index("idx_user_memberships_order_no", "order_no"),
        Index("idx_user_memberships_status_time", "status", "created_at"),
        Index("idx_user_memberships_end_at", "end_at"),
    )


class Coupon(Base):
    """优惠券表"""
    __tablename__ = "coupons"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="优惠券名称")
    description = Column(String(255), nullable=True, comment="描述")
    coupon_type = Column(Enum("fixed", "percent", "free_days"), nullable=False, comment="类型")
    value = Column(DECIMAL(10, 2), nullable=False, comment="优惠值")
    min_amount = Column(DECIMAL(10, 2), default=0.00, comment="最低使用金额")

    max_use_count = Column(BigInteger, nullable=True, comment="最大使用次数")
    used_count = Column(BigInteger, default=0, comment="已使用次数")
    user_limit = Column(BigInteger, default=1, comment="每人限领次数")

    valid_for_days = Column(BigInteger, nullable=True, comment="领取后有效天数")
    valid_from = Column(DateTime, nullable=True, comment="有效期开始")
    valid_to = Column(DateTime, nullable=True, comment="有效期结束")

    applicable_memberships = Column(JSON, nullable=True, comment="适用会员等级")
    applicable_products = Column(JSON, nullable=True, comment="适用商品类型")

    status = Column(Enum("active", "inactive", "expired"), default="active", comment="状态")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_coupons_status", "status"),
    )


class UserCoupon(Base):
    """用户优惠券表"""
    __tablename__ = "user_coupons"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    coupon_id = Column(BigInteger, ForeignKey("coupons.id", ondelete="CASCADE"), nullable=False, comment="优惠券ID")
    coupon_code = Column(String(50), nullable=False, unique=True, comment="券码")

    status = Column(Enum("unused", "used", "expired", "invalid"), default="unused", comment="状态")
    used_at = Column(DateTime, nullable=True, comment="使用时间")
    used_order_no = Column(String(50), nullable=True, comment="使用订单号")

    valid_from = Column(DateTime, nullable=False, comment="有效期开始")
    valid_to = Column(DateTime, nullable=False, comment="有效期结束")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_user_coupons_user_id", "user_id"),
        Index("idx_user_coupons_status_time", "status", "valid_to"),
        Index("idx_user_coupons_coupon_id", "coupon_id"),
    )