"""
素材 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.asset import *
from app.schemas.response import success_response, error_response
from app.services.asset_service import AssetService
from app.core.exceptions import NotFoundException

router = APIRouter()


# 用户素材
@router.get("")
def get_user_assets(
    asset_type: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取用户素材列表"""
    result = AssetService.get_user_assets(
        db, user_id, asset_type, category, tag, keyword, page, page_size
    )
    return success_response(result)


@router.post("/token")
def get_upload_token(
    request: UploadTokenRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取上传凭证"""
    result = AssetService.get_upload_token(
        db, user_id, request.file_name, request.file_size, request.asset_type
    )
    return success_response(result)


@router.post("/{asset_id}/confirm")
def confirm_upload(
    asset_id: int,
    request: ConfirmUploadRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """确认上传完成"""
    try:
        data = request.model_dump()
        asset = AssetService.confirm_upload(db, user_id, asset_id, data)
        return success_response({"id": asset.id, "name": asset.name})
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.patch("/{asset_id}")
def update_asset(
    asset_id: int,
    request: UpdateAssetRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """更新素材信息"""
    try:
        data = request.model_dump(exclude_unset=True)
        asset = AssetService.update_asset(db, user_id, asset_id, data)
        return success_response({"id": asset.id, "name": asset.name})
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """删除素材"""
    AssetService.delete_asset(db, user_id, asset_id)
    return success_response(message="删除成功")