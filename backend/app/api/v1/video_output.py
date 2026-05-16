"""
视频输出 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.video import ShareVideoRequest
from app.schemas.response import success_response, error_response
from app.services.video_service import VideoService
from app.models.video import VideoOutput

router = APIRouter()


@router.get("/{output_id}")
def get_video_output(
    output_id: int,
    db: Session = Depends(get_db)
):
    """获取视频输出"""
    return success_response({"id": output_id})


@router.get("/{project_id}/outputs")
def get_project_outputs(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取项目视频输出列表"""
    output = VideoService.get_video_output(db, project_id)
    if not output:
        return error_response(40405, "视频不存在")
    return success_response(output)


@router.get("/{output_id}/download")
def download_video(
    output_id: int,
    db: Session = Depends(get_db)
):
    """下载视频"""
    return success_response({"download_url": "https://cdn.example.com/video/1.mp4"})


@router.post("/{output_id}/share")
def share_video(
    output_id: int,
    request: ShareVideoRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """分享视频"""
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


# Public endpoint - no auth required
@router.get("/shared/{share_token}")
def get_shared_video(
    share_token: str,
    db: Session = Depends(get_db)
):
    """获取分享视频（公开接口，无需认证）"""
    output = db.query(VideoOutput).filter(VideoOutput.share_token == share_token).first()
    if not output:
        return error_response(40405, "分享不存在或已过期")
    return success_response({
        "video_url": output.video_url,
        "thumbnail_url": output.thumbnail_url,
        "duration": float(output.duration) if output.duration else 0,
        "has_password": output.share_password is not None
    })