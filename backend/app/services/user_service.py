"""
用户服务
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.user import User, UserDevice, UserOAuthBinding, UserLoginHistory
from app.models.wallet import UserWallet
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import NotFoundException, ValidationException


class UserService:
    """用户服务"""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """获取用户"""
        return db.query(User).filter(User.id == user_id, User.status == "active").first()

    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> Dict[str, Any]:
        """获取用户资料"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("用户不存在", code=40401)

        wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()

        # 计算配额
        from app.services.wallet_service import WalletService
        quota = WalletService.calculate_quota(db, user)

        return {
            "id": user.id,
            "phone": user.phone,
            "email": user.email,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "bio": user.bio,
            "real_name": user.real_name,
            "real_name_verified": user.real_name_verified == True,
            "membership_type": user.membership_type,
            "membership_expire_at": user.membership_expire_at,
            "quota": quota,
            "wallet": {
                "balance": wallet.balance if wallet else "0.00",
                "frozen_balance": wallet.frozen_balance if wallet else "0.00"
            },
            "created_at": user.created_at,
            "last_login_at": user.last_login_at
        }

    @staticmethod
    def update_profile(db: Session, user_id: int, data: Dict[str, Any]) -> User:
        """更新用户资料"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("用户不存在", code=40401)

        for key, value in data.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)

        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(db: Session, user_id: int, old_password: str, new_password: str) -> bool:
        """修改密码"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("用户不存在", code=40401)

        if not verify_password(old_password, user.password_hash):
            raise ValidationException("原密码错误", code=40005)

        user.password_hash = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def reset_password(phone: str, code: str, new_password: str) -> bool:
        """重置密码"""
        from app.services.auth_service import AuthService
        from app.models.user import User

        # 验证验证码
        if not AuthService.verify_sms_code(phone, code, "reset_password"):
            raise ValidationException("验证码错误或已过期")

        return True

    @staticmethod
    def bind_phone(db: Session, user_id: int, phone: str, code: str) -> bool:
        """绑定手机号"""
        from app.services.auth_service import AuthService

        # 验证验证码
        if not AuthService.verify_sms_code(phone, code, "bind_phone"):
            raise ValidationException("验证码错误或已过期")

        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("用户不存在", code=40401)

        # 检查手机号是否已被使用
        existing = db.query(User).filter(User.phone == phone, User.id != user_id).first()
        if existing:
            raise ValidationException("手机号已被其他账号绑定", code=40901)

        user.phone = phone
        user.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def unbind_phone(db: Session, user_id: int, phone: str, password: str) -> bool:
        """解绑手机号"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("用户不存在", code=40401)

        if not verify_password(password, user.password_hash):
            raise ValidationException("密码错误")

        user.phone = None
        user.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def get_user_devices(db: Session, user_id: int, status: str = None) -> List[Dict[str, Any]]:
        """获取用户设备列表"""
        query = db.query(UserDevice).filter(UserDevice.user_id == user_id)

        if status == "active":
            query = query.filter(UserDevice.is_active == True)
        elif status == "inactive":
            query = query.filter(UserDevice.is_active == "0")

        devices = query.order_by(UserDevice.last_active_at.desc()).all()

        return [
            {
                "id": d.id,
                "device_name": d.device_name,
                "device_type": d.device_type,
                "os_version": d.os_version,
                "last_active_at": d.last_active_at,
                "is_current": d.device_id is not None
            }
            for d in devices
        ]

    @staticmethod
    def remove_device(db: Session, user_id: int, device_id: int) -> bool:
        """移除设备"""
        device = db.query(UserDevice).filter(
            UserDevice.id == device_id,
            UserDevice.user_id == user_id
        ).first()

        if device:
            device.is_active = "0"
            db.commit()
        return True

    @staticmethod
    def get_oauth_bindings(db: Session, user_id: int) -> List[Dict[str, Any]]:
        """获取OAuth绑定列表"""
        bindings = db.query(UserOAuthBinding).filter(
            UserOAuthBinding.user_id == user_id
        ).all()

        return [
            {
                "id": b.id,
                "provider": b.provider,
                "nickname": b.nickname,
                "avatar_url": b.avatar_url,
                "binded_at": b.created_at
            }
            for b in bindings
        ]

    @staticmethod
    def unbind_oauth(db: Session, user_id: int, provider: str) -> bool:
        """解绑OAuth"""
        binding = db.query(UserOAuthBinding).filter(
            UserOAuthBinding.user_id == user_id,
            UserOAuthBinding.provider == provider
        ).first()

        if binding:
            db.delete(binding)
            db.commit()
        return True