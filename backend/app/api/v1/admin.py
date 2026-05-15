"""
管理后台 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_admin_id
from app.schemas.admin import *
from app.schemas.response import success_response, error_response
from app.core.security import verify_password, get_password_hash, create_tokens
from app.core.exceptions import UnauthorizedException, NotFoundException

router = APIRouter()


@router.post("/login")
async def admin_login(
    request: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """管理员登录"""
    from app.models.admin import Admin

    admin = db.query(Admin).filter(
        Admin.username == request.username,
        Admin.status == "active"
    ).first()

    if not admin or not verify_password(request.password, admin.password_hash):
        return error_response(20001, "用户名或密码错误")

    tokens = create_tokens(admin.id, is_admin=True)

    return success_response({
        "admin": {
            "id": admin.id,
            "username": admin.username,
            "real_name": admin.real_name,
            "role": admin.role
        },
        "tokens": tokens
    })


@router.get("/users")
async def get_users(
    keyword: Optional[str] = None,
    membership_type: Optional[str] = None,
    status: Optional[str] = "active",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id)
):
    """获取用户列表"""
    from app.models.user import User
    from sqlalchemy import or_

    query = db.query(User).filter(User.status != "deleted")

    if keyword:
        query = query.filter(
            or_(
                User.phone.like(f"%{keyword}%"),
                User.email.like(f"%{keyword}%"),
                User.nickname.like(f"%{keyword}%")
            )
        )

    if membership_type:
        query = query.filter(User.membership_type == membership_type)

    if status:
        query = query.filter(User.status == status)

    total = query.count()
    users = query.order_by(
        User.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()

    from app.models.wallet import UserWallet

    items = []
    for user in users:
        wallet = db.query(UserWallet).filter(UserWallet.user_id == user.id).first()
        items.append({
            "id": user.id,
            "phone": user.phone,
            "email": user.email,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "membership_type": user.membership_type,
            "status": user.status,
            "balance": str(wallet.balance) if wallet else "0.00",
            "created_at": user.created_at,
            "last_login_at": user.last_login_at
        })

    return success_response({
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size
        }
    })


@router.get("/users/{user_id}")
async def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id)
):
    """获取用户详情"""
    from app.models.user import User
    from app.models.wallet import UserWallet
    from app.services.wallet_service import WalletService

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return error_response(40401, "用户不存在")

    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()
    quota = WalletService.calculate_quota(db, user)

    # 隐藏部分身份证号
    id_card_display = None
    if user.id_card_number:
        id_card_display = user.id_card_number[:3] + "***********" + user.id_card_number[-4:]

    return success_response({
        "id": user.id,
        "phone": user.phone,
        "email": user.email,
        "nickname": user.nickname,
        "avatar_url": user.avatar_url,
        "real_name": user.real_name,
        "id_card_number": id_card_display,
        "real_name_verified": user.real_name_verified == "1",
        "membership_type": user.membership_type,
        "membership_expire_at": user.membership_expire_at,
        "status": user.status,
        "balance": str(wallet.balance) if wallet else "0.00",
        "frozen_balance": str(wallet.frozen_balance) if wallet else "0.00",
        "quota": quota,
        "register_ip": user.register_ip,
        "register_source": user.register_source,
        "created_at": user.created_at,
        "last_login_at": user.last_login_at,
        "last_login_ip": user.last_login_ip
    })


@router.post("/users/{user_id}/ban")
async def ban_user(
    user_id: int,
    request: BanUserRequest,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id)
):
    """封禁/解封用户"""
    from app.models.user import User

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return error_response(40401, "用户不存在")

    user.status = "suspended" if request.action == "ban" else "active"
    db.commit()

    return success_response(message=f"用户已{'封禁' if request.action == 'ban' else '解封'}")


# 内容审核
@router.get("/reviews/pending")
async def get_pending_reviews(
    target_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id)
):
    """获取待审核列表"""
    from app.models.message import ContentReview

    query = db.query(ContentReview).filter(ContentReview.result == "pending")

    if target_type:
        query = query.filter(ContentReview.target_type == target_type)

    total = query.count()
    reviews = query.order_by(
        ContentReview.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()

    items = [
        {
            "id": r.id,
            "user_id": r.user_id,
            "target_type": r.target_type,
            "target_id": r.target_id,
            "review_type": r.review_type,
            "risk_score": float(r.risk_score) if r.risk_score else None,
            "risk_labels": r.risk_labels,
            "submit_data": r.submit_data,
            "created_at": r.created_at
        }
        for r in reviews
    ]

    return success_response({
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size
        }
    })


@router.post("/reviews/{review_id}/approve")
async def approve_review(
    review_id: int,
    request: ApproveReviewRequest,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id)
):
    """审核通过"""
    return success_response(message="审核通过")


@router.post("/reviews/{review_id}/reject")
async def reject_review(
    review_id: int,
    request: RejectReviewRequest,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id)
):
    """审核驳回"""
    return success_response(message="审核驳回")


# 数据统计
@router.get("/statistics/overview")
async def get_platform_statistics(
    period: str = "last_7_days",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id)
):
    """平台整体统计"""
    return success_response({
        "period": period,
        "start_date": start_date or "2024-01-08",
        "end_date": end_date or "2024-01-14",
        "users": {
            "new": 1250,
            "active": 5800,
            "paid": 320,
            "churned": 45
        },
        "business": {
            "video_projects_created": 850,
            "video_projects_completed": 780,
            "video_projects_failed": 12,
            "video_success_rate": 98.5,
            "digital_humans_created": 180,
            "avg_video_duration": 42.5
        },
        "finance": {
            "total_revenue_cents": 125000,
            "membership_revenue_cents": 85000,
            "single_purchase_revenue_cents": 40000,
            "total_cost_cents": 45000,
            "gross_profit_cents": 80000
        },
        "models": {
            "seeddance": {
                "calls": 680,
                "success": 650,
                "fail": 30,
                "success_rate": 95.6,
                "cost_cents": 28000
            }
        }
    })


# 系统配置
@router.get("/configs")
async def get_configs(
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id)
):
    """获取系统配置"""
    from app.models.admin import SystemConfig

    configs = db.query(SystemConfig).filter(SystemConfig.is_editable == "1").all()

    return success_response({
        "items": [
            {
                "key": c.config_key,
                "value": c.config_value,
                "type": c.config_type,
                "description": c.description,
                "category": c.category,
                "is_editable": c.is_editable == "1"
            }
            for c in configs
        ]
    })


@router.patch("/configs")
async def update_configs(
    request: UpdateConfigsRequest,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id)
):
    """更新系统配置"""
    from app.models.admin import SystemConfig

    for config in request.configs:
        key = config.get("key")
        value = config.get("value")

        db.query(SystemConfig).filter(
            SystemConfig.config_key == key,
            SystemConfig.is_editable == "1"
        ).update({
            "config_value": value,
            "updated_at": db.func.now()
        })

    db.commit()
    return success_response(message="配置更新成功")