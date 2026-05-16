"""
声音克隆 API
"""
from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.voice import *
from app.schemas.response import success_response, error_response
from app.services.voice_service import VoiceService
from app.core.exceptions import NotFoundException

router = APIRouter()


@router.get("")
def get_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取声音克隆列表"""
    result = VoiceService.get_list(db, user_id, page, page_size)
    return success_response(result)


@router.post("")
def create(
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


@router.post("/preview")
def preview_tts(
    request: PreviewTTSRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """TTS 预览 - 使用指定音色预览文本转语音结果"""
    try:
        result = VoiceService.preview_tts(db, user_id, request.text, request.voice_id, request.config)
        return success_response(result)
    except NotFoundException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.get("/{voice_id}/set-default")
def set_default(
    voice_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """设置默认音色"""
    VoiceService.set_default(db, user_id, voice_id)
    return success_response(message="设置成功")


@router.delete("/{voice_id}")
def delete(
    voice_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """删除声音克隆"""
    VoiceService.delete(db, user_id, voice_id)
    return success_response(message="删除成功")