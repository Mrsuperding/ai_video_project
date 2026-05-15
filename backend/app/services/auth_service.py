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


class AuthService:
    """认证服务"""

    @staticmethod
    def generate_sms_code(length: int = 6) -> str:
        """生成短信验证码"""
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def send_sms_code(phone: str, code_type: str, ip_address: str = None, device_id: str = None) -> Dict[str, Any]:
        """
        发送短信验证码
        实际实现需要接入短信服务商
        """
        code = AuthService.generate_sms_code()
        # TODO: 调用短信服务商API发送验证码
        # 这里存储验证码到Redis或数据库用于验证
        return {
            "code": code,  # 实际不返回验证码，仅用于测试
            "expire_seconds": 300,
            "retry_after": 60
        }

    @staticmethod
    def verify_sms_code(phone: str, code: str, code_type: str) -> bool:
        """
        验证短信验证码
        实际实现从Redis或数据库读取验证码进行比对
        """
        # TODO: 从Redis或数据库验证验证码
        # 这里简化为任何6位数字验证码都有效
        return len(code) == 6 and code.isdigit()

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
            # 创建新用户
            user = User(
                phone=phone,
                nickname=f"用户{random.randint(1000, 9999)}",
                password_hash=get_password_hash(str(random.randint(100000, 999999))),
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