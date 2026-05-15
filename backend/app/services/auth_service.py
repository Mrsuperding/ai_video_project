"""
认证服务
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import random
import string

from app.models.user import User, UserLoginHistory
from app.models.wallet import UserWallet, UserWalletTransaction
from app.core.security import verify_password, get_password_hash, create_tokens
from app.core.exceptions import ValidationException, UnauthorizedException, ConflictException
from app.redis import get_sync_redis


class AuthService:
    """认证服务"""

    SMS_CODE_PREFIX = "sms:{phone}:{code_type}"
    SMS_CODE_TTL = 300  # 5 minutes

    @staticmethod
    def generate_sms_code(length: int = 6) -> str:
        """生成短信验证码"""
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def send_sms_code(phone: str, code_type: str, ip_address: str = None, device_id: str = None) -> Dict[str, Any]:
        """
        发送短信验证码
        将验证码存储到 Redis
        """
        code = AuthService.generate_sms_code()

        # 存储验证码到 Redis
        redis_client = get_sync_redis()
        if redis_client:
            key = f"sms:{phone}:{code_type}"
            redis_client.setex(key, AuthService.SMS_CODE_TTL, code)

        # TODO: 调用短信服务商API发送验证码
        return {
            "expire_seconds": 300,
            "retry_after": 60
        }

    @staticmethod
    def verify_sms_code(phone: str, code: str, code_type: str) -> bool:
        """
        验证短信验证码
        从 Redis 获取并比对验证码
        """
        redis_client = get_sync_redis()
        if not redis_client:
            # 如果 Redis 不可用，降级为简单验证（仅用于测试）
            return len(code) == 6 and code.isdigit()

        key = f"sms:{phone}:{code_type}"
        stored_code = redis_client.get(key)

        if not stored_code:
            return False

        # 验证码匹配后删除（一次性使用）
        if stored_code == code:
            redis_client.delete(key)
            return True

        return False

    @staticmethod
    def sms_login(
        db: Session,
        phone: str,
        code: str,
        code_type: str = "login",
        device_id: str = None,
        device_type: str = "web",
        ip_address: str = None,
        user_agent: str = None
    ) -> Tuple[User, Dict[str, Any], bool]:
        """
        短信验证码登录/注册
        """
        # 验证验证码
        if not AuthService.verify_sms_code(phone, code, code_type):
            raise ValidationException("验证码错误或已过期")

        # 查找或创建用户
        user = db.query(User).filter(User.phone == phone).first()
        is_new_user = False

        if not user:
            is_new_user = True
            # 创建新用户（手机注册用户不需要设置初始密码）
            user = User(
                phone=phone,
                nickname=f"用户{random.randint(1000, 9999)}",
                password_hash=None,  # 手机用户通过验证码登录，不需要密码
                register_ip=ip_address,
                register_source="web" if device_type == "web" else "mobile"
            )
            db.add(user)
            db.flush()

            # 创建钱包
            wallet = UserWallet(user_id=user.id)
            db.add(wallet)

        # 更新登录信息
        user.last_login_at = datetime.utcnow()
        user.last_login_ip = ip_address

        # 记录登录历史
        login_history = UserLoginHistory(
            user_id=user.id,
            login_type="sms",
            device_type=device_type,
            device_id=device_id,
            ip_address=ip_address or "0.0.0.0",
            user_agent=user_agent
        )
        db.add(login_history)
        db.commit()

        # 生成Token
        tokens = create_tokens(user.id)

        return user, tokens, is_new_user

    @staticmethod
    def password_login(
        db: Session,
        account: str,
        password: str,
        device_id: str = None,
        device_type: str = "web",
        ip_address: str = None,
        user_agent: str = None
    ) -> Tuple[User, Dict[str, Any]]:
        """
        密码登录
        """
        # 查找用户
        user = db.query(User).filter(
            (User.phone == account) | (User.email == account),
            User.status == "active"
        ).first()

        if not user:
            raise UnauthorizedException("账号或密码错误", code=20001)

        # 检查密码是否设置
        if not user.password_hash:
            raise UnauthorizedException("请使用短信验证码登录", code=20002)

        # 验证密码
        if not verify_password(password, user.password_hash):
            raise UnauthorizedException("账号或密码错误", code=20001)

        # 更新登录信息
        user.last_login_at = datetime.utcnow()
        user.last_login_ip = ip_address

        # 记录登录历史
        login_history = UserLoginHistory(
            user_id=user.id,
            login_type="password",
            device_type=device_type,
            device_id=device_id,
            ip_address=ip_address or "0.0.0.0",
            user_agent=user_agent
        )
        db.add(login_history)
        db.commit()

        # 生成Token
        tokens = create_tokens(user.id)

        return user, tokens

    @staticmethod
    def refresh_token(refresh_token: str) -> Dict[str, Any]:
        """
        刷新Token
        """
        from app.core.security import decode_token

        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid refresh token", code=20003)

        user_id = payload.get("user_id")
        if not user_id:
            raise UnauthorizedException("Invalid refresh token", code=20003)

        # 生成新Token
        tokens = create_tokens(user_id)
        return tokens

    @staticmethod
    def logout(user_id: int):
        """登出"""
        # TODO: 将Token加入黑名单
        pass