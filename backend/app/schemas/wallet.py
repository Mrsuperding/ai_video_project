"""
钱包相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WalletResponse(BaseModel):
    """钱包响应"""
    balance: str
    frozen_balance: str
    total_recharge: str
    total_consume: str


class TransactionItem(BaseModel):
    """交易记录项"""
    id: int
    transaction_no: str
    transaction_type: str
    amount: str
    balance_before: str
    balance_after: str
    related_type: Optional[str] = None
    related_id: Optional[int] = None
    remark: Optional[str] = None
    created_at: datetime


class RechargeRequest(BaseModel):
    """充值请求"""
    amount: str = Field(..., gt="0", description="充值金额")
    payment_method: str = Field(..., description="支付方式: alipay/wechat/stripe")


class RechargeResponse(BaseModel):
    """充值响应"""
    order_no: str
    amount: str
    payment_method: str
    payment_info: dict
    created_at: datetime


class RechargeStatusResponse(BaseModel):
    """充值状态响应"""
    order_no: str
    amount: str
    status: str
    paid_at: Optional[datetime] = None


class MembershipPlan(BaseModel):
    """会员套餐"""
    id: int
    name: str
    type: str
    original_price: str
    price: str
    duration_months: int
    quota: dict
    features: List[str]


class SubscribeRequest(BaseModel):
    """订阅请求"""
    plan_id: int
    duration_months: int = 1
    payment_method: str = Field(..., description="支付方式")
    coupon_code: Optional[str] = None


class SubscribeResponse(BaseModel):
    """订阅响应"""
    order_no: str
    original_price: str
    discount_amount: str
    actual_price: str
    plan: MembershipPlan
    payment_info: dict


class MembershipInfo(BaseModel):
    """会员信息"""
    membership_type: str
    start_at: datetime
    end_at: datetime
    days_remaining: int
    auto_renew: bool
    quota: dict


class CouponInfo(BaseModel):
    """优惠券信息"""
    id: int
    name: str
    description: Optional[str] = None
    coupon_type: str
    value: str
    min_amount: str
    valid_to: datetime
    applicable_products: Optional[List[str]] = None


class UserCouponInfo(BaseModel):
    """用户优惠券信息"""
    id: int
    coupon_code: str
    name: str
    coupon_type: str
    value: str
    status: str
    valid_from: datetime
    valid_to: datetime