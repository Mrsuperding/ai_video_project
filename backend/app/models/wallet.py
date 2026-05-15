"""
钱包相关模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, DECIMAL, Index
from sqlalchemy.sql import func
from app.database import Base


class UserWallet(Base):
    """用户钱包表"""
    __tablename__ = "user_wallets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, unique=True, comment="用户ID")
    balance = Column(DECIMAL(12, 4), default=0.0000, comment="账户余额")
    frozen_balance = Column(DECIMAL(12, 4), default=0.0000, comment="冻结余额")
    total_recharge = Column(DECIMAL(12, 4), default=0.0000, comment="累计充值金额")
    total_consume = Column(DECIMAL(12, 4), default=0.0000, comment="累计消费金额")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class UserWalletTransaction(Base):
    """用户钱包流水表"""
    __tablename__ = "user_wallet_transactions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    transaction_no = Column(String(50), nullable=False, unique=True, comment="交易流水号")
    transaction_type = Column(Enum("recharge", "consume", "refund", "recharge_refund", "invite_reward", "admin_adjust"), nullable=False, comment="交易类型")
    amount = Column(DECIMAL(12, 4), nullable=False, comment="交易金额")
    balance_before = Column(DECIMAL(12, 4), nullable=False, comment="交易前余额")
    balance_after = Column(DECIMAL(12, 4), nullable=False, comment="交易后余额")
    related_type = Column(String(50), nullable=True, comment="关联类型")
    related_id = Column(BigInteger, nullable=True, comment="关联ID")
    remark = Column(String(255), nullable=True, comment="备注")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_transaction_no", "transaction_no"),
        Index("idx_type_time", "transaction_type", "created_at"),
    )