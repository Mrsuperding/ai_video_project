"""
平台素材 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.response import success_response
from app.services.asset_service import AssetService

router = APIRouter()


@router.get("/list")
async def get_platform_assets(
    asset_type: Optional[str] = None,
    category: Optional[str] = None,
    license_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取平台素材列表"""
    result = AssetService.get_platform_assets(db, asset_type, category, license_type, page, page_size)
    return success_response(result)


@router.get("/categories")
async def get_categories(
    asset_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取素材分类"""
    categories = AssetService.get_categories(db, asset_type)
    return success_response({"items": categories})