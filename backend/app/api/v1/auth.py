"""
认证 API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.auth import *
from app.schemas.response import success_response, error_response
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.core.security import create_tokens
from app.core.exceptions import ValidationException, UnauthorizedException
from app.core.limiter import check_rate_limit, sms_limiter, login_limiter

router = APIRouter()


@router.post("/sms/send")
async def send_sms_code(
    request: SendSmsCodeRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """发送短信验证码"""
    # 限流：每手机号每5分钟1次
    client_ip = http_request.client.host if http_request.client else "unknown"
    await check_rate_limit(sms_limiter, request.phone)

    result = AuthService.send_sms_code(
        phone=request.phone,
        code_type=request.code_type,
        ip_address=client_ip,
        device_id=request.device_id
    )
    return success_response(result)


@router.post("/login/sms")
async def sms_login(
    request: SmsLoginRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """手机号验证码登录/注册"""
    # 限流：每IP每分钟3次
    client_ip = http_request.client.host if http_request.client else "unknown"
    await check_rate_limit(login_limiter, client_ip)

    try:
        user, tokens, is_new = AuthService.sms_login(
            db=db,
            phone=request.phone,
            code=request.code,
            code_type="login",
            device_id=request.device_id,
            device_type=request.device_type
        )

        # 获取用户配额信息
        from app.services.wallet_service import WalletService
        quota = WalletService.calculate_quota(db, user)

        user_info = {
            "id": user.id,
            "phone": user.phone,
            "email": user.email,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "bio": user.bio,
            "membership_type": user.membership_type,
            "membership_expire_at": user.membership_expire_at,
            "quota": quota,
            "created_at": user.created_at
        }

        return success_response({
            "user": user_info,
            "tokens": tokens,
            "is_new_user": is_new
        })
    except ValidationException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.post("/login/password")
async def password_login(
    request: PasswordLoginRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """密码登录"""
    # 限流：每IP每分钟3次
    client_ip = http_request.client.host if http_request.client else "unknown"
    await check_rate_limit(login_limiter, client_ip)

    try:
        user, tokens = AuthService.password_login(
            db=db,
            account=request.account,
            password=request.password,
            device_id=request.device_id,
            device_type=request.device_type
        )

        from app.services.wallet_service import WalletService
        quota = WalletService.calculate_quota(db, user)

        user_info = {
            "id": user.id,
            "phone": user.phone,
            "email": user.email,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "bio": user.bio,
            "membership_type": user.membership_type,
            "membership_expire_at": user.membership_expire_at,
            "quota": quota,
            "created_at": user.created_at
        }

        return success_response({
            "user": user_info,
            "tokens": tokens,
            "is_new_user": False
        })
    except UnauthorizedException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.post("/login/oauth")
async def oauth_login(
    request: OAuthLoginRequest,
    db: Session = Depends(get_db)
):
    """OAuth登录"""
    # TODO: 实现OAuth登录
    return error_response(50001, "OAuth登录暂未开放")


@router.post("/refresh")
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """刷新Token"""
    try:
        tokens = AuthService.refresh_token(request.refresh_token)
        return success_response(tokens)
    except UnauthorizedException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.post("/logout")
async def logout(
    user_id: int = Depends(get_current_user_id)
):
    """登出"""
    AuthService.logout(user_id)
    return success_response(message="登出成功")