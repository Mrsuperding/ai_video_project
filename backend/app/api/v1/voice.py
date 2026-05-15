"""
声音克隆 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.voice import *
from app.schemas.response import success_response, error_response
from app.services.voice_service import VoiceService
from app.core.exceptions import NotFoundException

router = APIRouter()


@router.get("")
async def get_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取声音克隆列表"""
    result = VoiceService.get_list(db, user_id, page, page_size)
    return success_response(result)


@router.post("")
async def create(
    request: CreateVoiceCloneRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """创建声音克隆"""
    try:
        data = request.model_dump()
        result = VoiceService.create(db, user_id, data)
        return success_response(result, message="声音克隆任务已创建")
    except Exception as e:
        return error_response(50001, str(e))


@router.post("/{voice_id}/set-default")
async def set_default(
    voice_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """设置默认音色"""
    VoiceService.set_default(db, user_id, voice_id)
    return success_response(message="设置成功")


@router.delete("/{voice_id}")
async def delete(
    voice_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """删除声音克隆"""
    VoiceService.delete(db, user_id, voice_id)
    return success_response(message="删除成功")