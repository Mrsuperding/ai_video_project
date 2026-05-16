"""
数字人 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.digital_human import *
from app.schemas.response import success_response, error_response
from app.services.digital_human_service import DigitalHumanService
from app.core.exceptions import NotFoundException, QuotaExceededException

router = APIRouter()


@router.get("")
def get_list(
    status: str = "all",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取数字人列表"""
    result = DigitalHumanService.get_list(db, user_id, status, page, page_size)
    return success_response(result)


@router.get("/{digital_human_id}")
def get_detail(
    digital_human_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取数字人详情"""
    try:
        detail = DigitalHumanService.get_detail(db, user_id, digital_human_id)
        return success_response(detail)
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.post("")
def create(
    request: CreateDigitalHumanRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """创建数字人"""
    try:
        data = request.model_dump()
        # 转换source_photos
        if request.source_photos:
            data["source_photos"] = [p.model_dump() for p in request.source_photos]

        result = DigitalHumanService.create(db, user_id, data)
        return success_response(result, message="数字人创建成功，正在生成中")
    except QuotaExceededException as e:
        return error_response(e.code, e.message)
    except Exception as e:
        return error_response(50001, str(e))


@router.patch("/{digital_human_id}")
def update(
    digital_human_id: int,
    request: UpdateDigitalHumanRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """更新数字人信息"""
    try:
        data = request.model_dump(exclude_unset=True)
        dh = DigitalHumanService.update(db, user_id, digital_human_id, data)
        return success_response({
            "id": dh.id,
            "name": dh.name,
            "description": dh.description
        })
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.post("/{digital_human_id}/regenerate")
def regenerate(
    digital_human_id: int,
    request: RegenerateRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """重新生成数字人"""
    try:
        new_photos = [p.model_dump() for p in request.new_photos]
        result = DigitalHumanService.regenerate(db, user_id, digital_human_id, new_photos)
        return success_response(result, message="任务已创建")
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.post("/{digital_human_id}/set-default")
def set_default(
    digital_human_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """设置默认数字人"""
    DigitalHumanService.set_default(db, user_id, digital_human_id)
    return success_response(message="设置成功")


@router.delete("/{digital_human_id}")
def delete(
    digital_human_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """删除数字人"""
    DigitalHumanService.delete(db, user_id, digital_human_id)
    return success_response(message="删除成功", data={"retention_days": 30, "can_restore": True})


@router.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取任务状态"""
    try:
        task = DigitalHumanService.get_task(db, user_id, task_id)
        return success_response(task)
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.post("/upload/token")
def get_upload_token(
    request: dict,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取上传凭证"""
    return success_response({
        "upload_token": "token_abc123",
        "upload_url": "https://upload.example.com/upload",
        "expire_seconds": 3600,
        "file_prefix": f"dh_{user_id}_20240115_"
    })


@router.post("/check-photos")
def check_photos(
    request: dict,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """照片检查 - 检查上传的照片是否符合要求"""
    photo_urls = request.get("photo_urls", [])
    if not photo_urls:
        return error_response(40001, "照片URL列表不能为空")

    results = DigitalHumanService.check_photos(db, user_id, photo_urls)
    return success_response(results)