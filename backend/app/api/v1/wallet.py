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
def get_wallet(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取钱包信息"""
    wallet = WalletService.get_wallet(db, user_id)
    return success_response(wallet)


@router.get("/transactions")
def get_transactions(
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
def create_recharge(
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
def get_recharge_status(
    order_no: str,
    db: Session = Depends(get_db)
):
    """查询充值订单状态"""
    status = WalletService.get_recharge_status(db, order_no)
    return success_response(status)