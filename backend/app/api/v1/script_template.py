"""
脚本模板 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.response import success_response, error_response
from app.services.script_service import ScriptService
from app.core.exceptions import NotFoundException

router = APIRouter()


@router.get("/list")
def get_templates(
    category: Optional[str] = None,
    source: str = "platform",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取模板列表"""
    result = ScriptService.get_templates(db, category, source, page, page_size)
    return success_response(result)


@router.get("/{template_id}")
def get_template_detail(
    template_id: int,
    db: Session = Depends(get_db)
):
    """获取模板详情"""
    try:
        detail = ScriptService.get_template_detail(db, template_id)
        return success_response(detail)
    except NotFoundException as e:
        return error_response(e.code, e.message)