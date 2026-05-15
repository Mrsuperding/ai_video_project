"""
钱包 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.wallet import *
from app.schemas.response import success_response, error_response
from app.services.wallet_service import WalletService
from app.core.exceptions import NotFoundException, QuotaExceededException

router = APIRouter()


@router.get("")
async def get_wallet(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取钱包信息"""
    wallet = WalletService.get_wallet(db, user_id)
    return success_response(wallet)


@router.get("/transactions")
async def get_transactions(
    transaction_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取钱包流水"""
    transactions = WalletService.get_transactions(
        db, user_id, transaction_type, start_date, end_date, page, page_size
    )
    return success_response(transactions)


@router.post("/recharge")
async def create_recharge(
    request: RechargeRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """创建充值订单"""
    try:
        order = WalletService.create_recharge_order(
            db, user_id, request.amount, request.payment_method
        )
        return success_response(order)
    except Exception as e:
        return error_response(50001, str(e))


@router.get("/recharge/{order_no}")
async def get_recharge_status(
    order_no: str,
    db: Session = Depends(get_db)
):
    """查询充值订单状态"""
    status = WalletService.get_recharge_status(db, order_no)
    return success_response(status)


# 会员相关
@router.get("/plans")
async def get_membership_plans(
    db: Session = Depends(get_db)
):
    """获取会员套餐列表"""
    plans = [
        {
            "id": 1,
            "name": "基础版",
            "type": "basic",
            "original_price": "99.00",
            "price": "99.00",
            "duration_months": 1,
            "quota": {
                "digital_human": 10,
                "video_monthly": 50,
                "video_max_duration": 180,
                "storage_mb": 2048
            },
            "features": ["1080p高清输出", "去水印", "优先渲染队列"]
        },
        {
            "id": 2,
            "name": "专业版",
            "type": "pro",
            "original_price": "299.00",
            "price": "199.00",
            "duration_months": 1,
            "quota": {
                "digital_human": 100,
                "video_monthly": 500,
                "video_max_duration": 300,
                "storage_mb": 10240
            },
            "features": ["4K超清输出", "去水印", "优先渲染队列", "API调用权限", "客户支持"]
        }
    ]
    return success_response({"items": plans})


@router.post("/subscribe")
async def subscribe(
    request: SubscribeRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """创建会员订单"""
    # TODO: 实现会员订阅
    return success_response({
        "order_no": "MBR20240115001001",
        "original_price": "299.00",
        "discount_amount": "0.00",
        "actual_price": "299.00",
        "plan": {"id": request.plan_id, "name": "专业版", "type": "pro", "duration_months": 1},
        "payment_info": {"qr_code": "https://qr.alipay.com/xxx", "expire_time": "2024-01-15T11:30:00Z"}
    })


@router.get("/orders/{order_no}")
async def get_membership_order(
    order_no: str,
    db: Session = Depends(get_db)
):
    """查询会员订单状态"""
    return success_response({
        "order_no": order_no,
        "status": "paid",
        "paid_at": "2024-01-15T10:35:00Z"
    })


@router.get("/my")
async def get_my_membership(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取我的会员信息"""
    from app.models.user import User
    user = db.query(User).filter(User.id == user_id).first()

    from datetime import datetime, timedelta
    return success_response({
        "membership_type": user.membership_type if user else "free",
        "start_at": datetime.utcnow(),
        "end_at": datetime.utcnow() + timedelta(days=365),
        "days_remaining": 365,
        "auto_renew": False,
        "quota": {
            "digital_human": {"total": 3, "used": 0, "remaining": 3},
            "video_monthly": {"total": 10, "used": 0, "remaining": 10},
            "video_max_duration": 60,
            "storage_mb": {"total": 1024, "used": 0, "remaining": 1024}
        }
    })


# 优惠券相关
@router.get("/available")
async def get_available_coupons(
    product_type: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取可用优惠券列表"""
    return success_response({"items": []})


@router.post("/{coupon_id}/claim")
async def claim_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """领取优惠券"""
    return success_response({
        "id": 101,
        "coupon_code": "COUPON2024011501",
        "valid_from": "2024-01-15T00:00:00Z",
        "valid_to": "2024-02-14T23:59:59Z"
    })


@router.get("/my")
async def get_my_coupons(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取我的优惠券"""
    return success_response({"items": []})