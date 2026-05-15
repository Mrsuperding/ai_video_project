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
async def get_projects(
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
async def get_project_detail(
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
async def create_project(
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
async def submit_generate(
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
async def cancel_generate(
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
async def update_project(
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
async def regenerate_project(
    project_id: int,
    request: RegenerateProjectRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """基于项目重新生成"""
    return success_response({"message": "功能开发中"})


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """删除项目"""
    VideoService.delete_project(db, user_id, project_id)
    return success_response(message="删除成功")


@router.post("/batch")
async def batch_operation(
    request: BatchOperationRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """批量操作"""
    return success_response({"message": f"批量{request.action}成功", "affected": len(request.project_ids)})


# 生成任务
@router.get("/task/{task_id}")
async def get_generation_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取任务状态"""
    try:
        task = VideoService.get_generation_task(db, user_id, task_id)
        return success_response(task)
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.get("/tasks")
async def get_tasks(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取任务列表"""
    return success_response({"items": []})


# 视频输出
@router.get("/output/{output_id}")
async def get_video_output(
    output_id: int,
    db: Session = Depends(get_db)
):
    """获取视频输出"""
    return success_response({"id": output_id})


@router.get("/{project_id}/output")
async def get_project_output(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取项目视频输出"""
    output = VideoService.get_video_output(db, project_id)
    if not output:
        return error_response(40405, "视频不存在")
    return success_response(output)


@router.get("/output/{output_id}/download")
async def download_video(
    output_id: int,
    db: Session = Depends(get_db)
):
    """下载视频"""
    return success_response({"download_url": "https://cdn.example.com/video/1.mp4"})


@router.post("/output/{output_id}/share")
async def share_video(
    output_id: int,
    request: ShareVideoRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """分享视频"""
    # 获取project_id
    from app.models.video import VideoOutput
    output = db.query(VideoOutput).filter(VideoOutput.id == output_id).first()
    if not output:
        return error_response(40405, "视频不存在")

    result = VideoService.share_video(
        db, output.project_id,
        request.expire_hours or 24,
        request.enable_password or False,
        request.password
    )
    return success_response(result)


@router.get("/share/{share_token}")
async def get_shared_video(
    share_token: str,
    db: Session = Depends(get_db)
):
    """获取分享视频"""
    from app.models.video import VideoOutput
    output = db.query(VideoOutput).filter(VideoOutput.share_token == share_token).first()
    if not output:
        return error_response(40405, "分享不存在或已过期")
    return success_response({
        "video_url": output.video_url,
        "thumbnail_url": output.thumbnail_url,
        "duration": float(output.duration) if output.duration else 0,
        "has_password": output.share_password is not None
    })