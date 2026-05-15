"""
优惠券 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.response import success_response

router = APIRouter()


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