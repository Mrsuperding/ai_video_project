"""
钱包服务
"""
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Optional, Dict, Any, List
from datetime import datetime, date
import uuid

from app.models.wallet import UserWallet, UserWalletTransaction
from app.models.user import User
from app.models.membership import UserMembership
from app.core.exceptions import NotFoundException, ValidationException, QuotaExceededException


class WalletService:
    """钱包服务"""

    @staticmethod
    def get_wallet(db: Session, user_id: int) -> Dict[str, Any]:
        """获取钱包信息"""
        wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()
        if not wallet:
            # 创建钱包
            wallet = UserWallet(user_id=user_id)
            db.add(wallet)
            db.commit()
            db.refresh(wallet)

        return {
            "balance": str(wallet.balance),
            "frozen_balance": str(wallet.frozen_balance),
            "total_recharge": str(wallet.total_recharge),
            "total_consume": str(wallet.total_consume)
        }

    @staticmethod
    def get_transactions(
        db: Session,
        user_id: int,
        transaction_type: str = None,
        start_date: str = None,
        end_date: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取钱包流水"""
        query = db.query(UserWalletTransaction).filter(
            UserWalletTransaction.user_id == user_id
        )

        if transaction_type:
            query = query.filter(UserWalletTransaction.transaction_type == transaction_type)

        if start_date:
            query = query.filter(
                UserWalletTransaction.created_at >= datetime.fromisoformat(start_date)
            )
        if end_date:
            query = query.filter(
                UserWalletTransaction.created_at <= datetime.fromisoformat(end_date)
            )

        total = query.count()
        transactions = query.order_by(
            UserWalletTransaction.created_at.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "items": [
                {
                    "id": t.id,
                    "transaction_no": t.transaction_no,
                    "transaction_type": t.transaction_type,
                    "amount": str(t.amount),
                    "balance_before": str(t.balance_before),
                    "balance_after": str(t.balance_after),
                    "related_type": t.related_type,
                    "related_id": t.related_id,
                    "remark": t.remark,
                    "created_at": t.created_at
                }
                for t in transactions
            ],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }

    @staticmethod
    def create_recharge_order(
        db: Session,
        user_id: int,
        amount: str,
        payment_method: str
    ) -> Dict[str, Any]:
        """创建充值订单"""
        order_no = f"REC{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"

        # TODO: 调用支付渠道创建订单

        return {
            "order_no": order_no,
            "amount": amount,
            "payment_method": payment_method,
            "payment_info": {
                "qr_code": "https://qr.alipay.com/xxx",
                "expire_time": (datetime.utcnow() + timedelta(hours=1)).isoformat()
            },
            "created_at": datetime.utcnow()
        }

    @staticmethod
    def get_recharge_status(db: Session, order_no: str) -> Dict[str, Any]:
        """查询充值订单状态"""
        # TODO: 查询支付渠道状态
        return {
            "order_no": order_no,
            "amount": "100.00",
            "status": "paid",
            "paid_at": datetime.utcnow()
        }

    @staticmethod
    def calculate_quota(db: Session, user: User) -> Dict[str, Any]:
        """计算用户配额"""
        # 计算视频配额
        today = date.today()
        start_of_month = today.replace(day=1)

        # 视频使用统计
        from app.models.video import VideoProject
        video_used = db.query(VideoProject).filter(
            VideoProject.user_id == user.id,
            VideoProject.generation_status.in_(["queued", "preprocessing", "generating", "postprocessing", "quality_check", "completed"]),
            VideoProject.created_at >= start_of_month
        ).count()

        # 数字人使用统计
        from app.models.digital_human import DigitalHuman
        dh_count = db.query(DigitalHuman).filter(
            DigitalHuman.user_id == user.id,
            DigitalHuman.status.in_(["completed"])
        ).count()

        # 存储使用统计
        from app.models.asset import UserAsset
        storage_used = db.query(UserAsset).filter(
            UserAsset.user_id == user.id,
            UserAsset.deleted_at.is_(None)
        ).with_entities(
            func.sum(UserAsset.file_size)
        ).scalar() or 0

        quota = {
            "digital_human": {
                "total": user.quota_digital_human,
                "used": dh_count,
                "remaining": max(0, user.quota_digital_human - dh_count),
                "reset_at": None
            },
            "video_monthly": {
                "total": user.quota_video_monthly,
                "used": video_used,
                "remaining": max(0, user.quota_video_monthly - video_used),
                "reset_at": datetime(today.year, today.month + 1, 1) if today.month < 12 else datetime(today.year + 1, 1, 1)
            },
            "video_max_duration": user.quota_video_max_duration,
            "storage_mb": {
                "total": user.quota_storage_mb,
                "used": storage_used // (1024 * 1024),
                "remaining": max(0, user.quota_storage_mb - storage_used // (1024 * 1024))
            }
        }

        return quota

    @staticmethod
    def consume_balance(
        db: Session,
        user_id: int,
        amount: str,
        related_type: str,
        related_id: int,
        remark: str = None
    ) -> bool:
        """扣除余额"""
        wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).with_for_update().first()
        if not wallet:
            raise NotFoundException("钱包不存在")

        amount_decimal = float(amount)
        if wallet.balance < amount_decimal:
            raise QuotaExceededException("余额不足", code=30002)

        # 记录交易
        transaction = UserWalletTransaction(
            user_id=user_id,
            transaction_no=f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}",
            transaction_type="consume",
            amount=-amount_decimal,
            balance_before=wallet.balance,
            balance_after=wallet.balance - amount_decimal,
            related_type=related_type,
            related_id=related_id,
            remark=remark
        )
        db.add(transaction)

        # 更新余额
        wallet.balance -= amount_decimal
        wallet.total_consume += amount_decimal

        db.commit()
        return True


from datetime import timedelta