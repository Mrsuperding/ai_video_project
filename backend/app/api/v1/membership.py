"""
会员 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.wallet import SubscribeRequest
from app.schemas.response import success_response
from app.models.user import User

router = APIRouter()


@router.get("/plans")
def get_membership_plans(db: Session = Depends(get_db)):
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
def subscribe(
    request: SubscribeRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """创建会员订单"""
    return success_response({
        "order_no": "MBR20240115001001",
        "original_price": "299.00",
        "discount_amount": "0.00",
        "actual_price": "299.00",
        "plan": {"id": request.plan_id, "name": "专业版", "type": "pro", "duration_months": 1},
        "payment_info": {"qr_code": "https://qr.alipay.com/xxx", "expire_time": "2024-01-15T11:30:00Z"}
    })


@router.get("/orders/{order_no}")
def get_membership_order(
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
def get_my_membership(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取我的会员信息"""
    user = db.query(User).filter(User.id == user_id).first()

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