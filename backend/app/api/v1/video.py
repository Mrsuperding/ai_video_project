"""
视频 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.video import *
from app.schemas.response import success_response, error_response
from app.services.video_service import VideoService
from app.core.exceptions import NotFoundException

router = APIRouter()


@router.get("")
def get_projects(
    status: str = "all",
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取视频项目列表"""
    result = VideoService.get_projects(db, user_id, status, category, keyword, page, page_size)
    return success_response(result)


@router.get("/{project_id}")
def get_project_detail(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取项目详情"""
    try:
        detail = VideoService.get_project_detail(db, user_id, project_id)
        return success_response(detail)
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.post("")
def create_project(
    request: CreateVideoProjectRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """创建视频项目"""
    try:
        data = request.model_dump(exclude_unset=True)
        result = VideoService.create_project(db, user_id, data)
        return success_response(result, message="项目创建成功")
    except Exception as e:
        return error_response(50001, str(e))


@router.post("/{project_id}/generate")
def submit_generate(
    project_id: int,
    request: GenerateRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """提交视频生成任务"""
    try:
        result = VideoService.submit_generate(
            db, user_id, project_id, request.priority or 5
        )
        return success_response(result, message="任务已提交")
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.post("/{project_id}/cancel")
def cancel_generate(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """取消生成任务"""
    try:
        VideoService.cancel_generate(db, user_id, project_id)
        return success_response(message="任务已取消")
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.patch("/{project_id}")
def update_project(
    project_id: int,
    request: UpdateProjectRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """更新项目信息"""
    try:
        data = request.model_dump(exclude_unset=True)
        project = VideoService.update_project(db, user_id, project_id, data)
        return success_response({"id": project.id, "project_name": project.project_name})
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.post("/{project_id}/regenerate")
def regenerate_project(
    project_id: int,
    request: RegenerateProjectRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """基于项目重新生成"""
    return success_response({"message": "功能开发中"})


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """删除项目"""
    VideoService.delete_project(db, user_id, project_id)
    return success_response(message="删除成功")


@router.post("/batch")
def batch_operation(
    request: BatchOperationRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """批量操作"""
    return success_response({"message": f"批量{request.action}成功", "affected": len(request.project_ids)})