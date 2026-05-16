"""
用户 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.user import *
from app.schemas.auth import *
from app.schemas.response import success_response, error_response
from app.services.user_service import UserService
from app.core.exceptions import NotFoundException, ValidationException

router = APIRouter()


@router.get("/profile")
def get_profile(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取当前用户信息"""
    try:
        profile = UserService.get_user_profile(db, user_id)
        return success_response(profile)
    except NotFoundException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.patch("/profile")
def update_profile(
    request: UpdateProfileRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """更新用户信息"""
    try:
        data = request.model_dump(exclude_unset=True)
        user = UserService.update_profile(db, user_id, data)
        return success_response({
            "id": user.id,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "bio": user.bio
        })
    except NotFoundException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.post("/password/change")
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """修改密码"""
    try:
        UserService.change_password(db, user_id, request.old_password, request.new_password)
        return success_response(message="密码修改成功")
    except ValidationException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.post("/password/reset")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """重置密码"""
    try:
        UserService.reset_password(request.phone, request.code, request.new_password)
        return success_response(message="密码重置成功")
    except ValidationException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.post("/phone/bind")
def bind_phone(
    request: BindPhoneRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """绑定手机号"""
    try:
        UserService.bind_phone(db, user_id, request.phone, request.code)
        return success_response(message="绑定成功")
    except ValidationException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.post("/phone/unbind")
def unbind_phone(
    request: UnbindPhoneRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """解绑手机号"""
    try:
        UserService.unbind_phone(db, user_id, request.phone, request.password)
        return success_response(message="解绑成功")
    except ValidationException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.get("/devices")
def get_devices(
    status: str = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取登录设备列表"""
    devices = UserService.get_user_devices(db, user_id, status)
    return success_response({"items": devices})


@router.delete("/devices/{device_id}")
def remove_device(
    device_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """退出登录设备"""
    UserService.remove_device(db, user_id, device_id)
    return success_response(message="设备已退出登录")


@router.get("/oauth-bindings")
def get_oauth_bindings(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取OAuth绑定列表"""
    bindings = UserService.get_oauth_bindings(db, user_id)
    return success_response({"items": bindings})


@router.delete("/oauth-bindings/{provider}")
def unbind_oauth(
    provider: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """解绑OAuth"""
    UserService.unbind_oauth(db, user_id, provider)
    return success_response(message="解绑成功")