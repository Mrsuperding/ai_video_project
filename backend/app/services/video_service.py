"""
视频服务
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.video import VideoProject, VideoOutput, GenerationTask
from app.models.digital_human import DigitalHuman
from app.core.exceptions import NotFoundException, QuotaExceededException


class VideoService:
    """视频服务"""

    @staticmethod
    def get_projects(
        db: Session,
        user_id: int,
        status: str = "all",
        category: str = None,
        keyword: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取视频项目列表"""
        query = db.query(VideoProject).filter(
            VideoProject.user_id == user_id,
            VideoProject.deleted_at.is_(None)
        )

        if status and status != "all":
            query = query.filter(VideoProject.generation_status == status)

        if category:
            query = query.filter(VideoProject.category == category)

        if keyword:
            query = query.filter(VideoProject.project_name.like(f"%{keyword}%"))

        total = query.count()
        items = query.order_by(
            VideoProject.created_at.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()

        result = []
        for project in items:
            item = {
                "id": project.id,
                "project_name": project.project_name,
                "description": project.description,
                "status": project.generation_status,
                "resolution": project.resolution,
                "aspect_ratio": project.aspect_ratio,
                "view_count": project.view_count,
                "download_count": project.download_count,
                "created_at": project.created_at,
                "updated_at": project.updated_at
            }

            # 获取数字人信息
            dh = db.query(DigitalHuman).filter(DigitalHuman.id == project.digital_human_id).first()
            if dh:
                item["digital_human"] = {
                    "id": dh.id,
                    "name": dh.name,
                    "preview_image_url": dh.preview_image_url
                }

            # 获取输出信息
            output = db.query(VideoOutput).filter(VideoOutput.project_id == project.id).first()
            if output:
                item["duration"] = float(output.duration) if output.duration else None
                item["thumbnail_url"] = output.thumbnail_url
            elif project.generation_status in ["queued", "preprocessing", "generating", "postprocessing", "quality_check"]:
                # 获取进行中的任务
                task = db.query(GenerationTask).filter(
                    GenerationTask.project_id == project.id,
                    GenerationTask.status.in_(["queued", "processing"])
                ).order_by(GenerationTask.created_at.desc()).first()
                if task:
                    item["progress"] = task.progress
                    item["estimated_remaining_seconds"] = 900  # 预估

            result.append(item)

        return {
            "items": result,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }

    @staticmethod
    def get_project_detail(db: Session, user_id: int, project_id: int) -> Dict[str, Any]:
        """获取项目详情"""
        project = db.query(VideoProject).filter(
            VideoProject.id == project_id,
            VideoProject.user_id == user_id,
            VideoProject.deleted_at.is_(None)
        ).first()

        if not project:
            raise NotFoundException("项目不存在", code=40405)

        result = {
            "id": project.id,
            "user_id": project.user_id,
            "project_name": project.project_name,
            "description": project.description,
            "resolution": project.resolution,
            "aspect_ratio": project.aspect_ratio,
            "fps": project.fps,
            "max_duration": project.max_duration,
            "generation_status": project.generation_status,
            "priority": project.priority,
            "digital_human_id": project.digital_human_id,
            "digital_human_config": project.digital_human_config,
            "script_id": project.script_id,
            "script_content": project.script_content,
            "voice_id": project.voice_id,
            "tts_config": project.tts_config,
            "background_asset_id": project.background_asset_id,
            "background_type": project.background_type,
            "background_value": project.background_value,
            "bgm_asset_id": project.bgm_asset_id,
            "bgm_volume": float(project.bgm_volume) if project.bgm_volume else 0.3,
            "subtitle_config": project.subtitle_config,
            "tags": project.tags,
            "category": project.category,
            "view_count": project.view_count,
            "download_count": project.download_count,
            "share_count": project.share_count,
            "cost_cents": project.cost_cents,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }

        # 获取输出信息
        output = db.query(VideoOutput).filter(VideoOutput.project_id == project_id).first()
        if output:
            result["output"] = {
                "id": output.id,
                "video_url": output.video_url,
                "thumbnail_url": output.thumbnail_url,
                "video_file_size": output.video_file_size,
                "resolution": output.resolution,
                "duration": float(output.duration) if output.duration else None,
                "fps": output.fps,
                "codec": output.codec,
                "bitrate": output.bitrate,
                "has_audio": output.has_audio == "1",
                "quality_score": output.quality_score,
                "review_status": output.review_status,
                "watermark_embedded": output.watermark_embedded == "1",
                "view_count": output.view_count,
                "download_count": output.download_count,
                "share_count": output.share_count,
                "created_at": output.created_at
            }

        return result

    @staticmethod
    def create_project(
        db: Session,
        user_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """创建视频项目"""
        project = VideoProject(
            user_id=user_id,
            project_name=data["project_name"],
            description=data.get("description"),
            resolution=data.get("resolution", "1080p"),
            aspect_ratio=data.get("aspect_ratio", "16:9"),
            fps=data.get("fps", 30),
            digital_human_id=data["digital_human_id"],
            digital_human_config=data.get("digital_human_config"),
            script_id=data["script_id"],
            script_content=data.get("script_content"),
            voice_id=data.get("voice_id"),
            tts_config=data.get("tts_config"),
            background_asset_id=data.get("background_asset_id"),
            background_type=data.get("background_type", "image"),
            background_value=data.get("background_value"),
            bgm_asset_id=data.get("bgm_asset_id"),
            bgm_volume=data.get("bgm_volume", 0.3),
            timeline_config=data.get("timeline_config"),
            subtitle_config=data.get("subtitle_config"),
            tags=data.get("tags"),
            category=data.get("category"),
            generation_status="draft",
            priority=data.get("priority", 5)
        )
        db.add(project)
        db.commit()
        db.refresh(project)

        return {
            "id": project.id,
            "project_name": project.project_name,
            "status": project.generation_status,
            "estimated_cost_cents": 50
        }

    @staticmethod
    def submit_generate(
        db: Session,
        user_id: int,
        project_id: int,
        priority: int = 5
    ) -> Dict[str, Any]:
        """提交视频生成"""
        project = db.query(VideoProject).filter(
            VideoProject.id == project_id,
            VideoProject.user_id == user_id
        ).first()

        if not project:
            raise NotFoundException("项目不存在", code=40405)

        # 创建生成任务
        task = GenerationTask(
            user_id=user_id,
            project_id=project_id,
            task_type="full_pipeline",
            status="queued",
            priority=priority,
            model_provider="seeddance",
            model_name="video_gen_v2",
            input_config={
                "digital_human_id": project.digital_human_id,
                "script_id": project.script_id,
                "resolution": project.resolution,
                "aspect_ratio": project.aspect_ratio
            }
        )
        db.add(task)

        project.generation_status = "queued"
        db.commit()
        db.refresh(task)

        return {
            "project_id": project_id,
            "task_id": task.id,
            "status": task.status,
            "queue_position": 5,
            "estimated_seconds": 900
        }

    @staticmethod
    def cancel_generate(db: Session, user_id: int, project_id: int) -> bool:
        """取消生成"""
        project = db.query(VideoProject).filter(
            VideoProject.id == project_id,
            VideoHuman.user_id == user_id
        ).first()

        if not project:
            raise NotFoundException("项目不存在", code=40405)

        # 取消进行中的任务
        db.query(GenerationTask).filter(
            GenerationTask.project_id == project_id,
            GenerationTask.status.in_(["queued", "processing"])
        ).update({"status": "cancelled"})

        project.generation_status = "draft"
        db.commit()
        return True

    @staticmethod
    def get_generation_task(db: Session, user_id: int, task_id: int) -> Dict[str, Any]:
        """获取生成任务状态"""
        task = db.query(GenerationTask).filter(
            GenerationTask.id == task_id,
            GenerationTask.user_id == user_id
        ).first()

        if not task:
            raise NotFoundException("任务不存在")

        project = db.query(VideoProject).filter(VideoProject.id == task.project_id).first()

        return {
            "id": task.id,
            "project_id": task.project_id,
            "project_name": project.project_name if project else None,
            "task_type": task.task_type,
            "status": task.status,
            "progress": task.progress,
            "current_step": task.current_step,
            "model_provider": task.model_provider,
            "model_name": task.model_name,
            "started_at": task.started_at,
            "estimated_remaining_seconds": 420 if task.status == "processing" else None
        }

    @staticmethod
    def get_video_output(db: Session, project_id: int) -> Optional[Dict[str, Any]]:
        """获取视频输出"""
        output = db.query(VideoOutput).filter(VideoOutput.project_id == project_id).first()
        if not output:
            return None

        return {
            "id": output.id,
            "project_id": output.project_id,
            "video_url": output.video_url,
            "thumbnail_url": output.thumbnail_url,
            "video_file_size": output.video_file_size,
            "resolution": output.resolution,
            "duration": float(output.duration) if output.duration else None,
            "fps": output.fps,
            "codec": output.codec,
            "bitrate": output.bitrate,
            "has_audio": output.has_audio == "1",
            "quality_score": output.quality_score,
            "review_status": output.review_status,
            "watermark_embedded": output.watermark_embedded == "1",
            "view_count": output.view_count,
            "download_count": output.download_count,
            "share_count": output.share_count,
            "created_at": output.created_at
        }

    @staticmethod
    def share_video(
        db: Session,
        project_id: int,
        expire_hours: int = 24,
        enable_password: bool = False,
        password: str = None
    ) -> Dict[str, Any]:
        """分享视频"""
        import secrets
        share_token = secrets.token_urlsafe(32)

        output = db.query(VideoOutput).filter(VideoOutput.project_id == project_id).first()
        if not output:
            raise NotFoundException("视频不存在")

        output.share_token = share_token
        output.share_enabled = "1"
        output.share_expire_at = datetime.utcnow().replace(hour=23, minute=59, second=59) + timedelta(hours=expire_hours)
        if enable_password:
            output.share_password = password

        db.commit()

        return {
            "share_url": f"https://platform.example.com/share/v/{share_token}",
            "share_token": share_token,
            "expire_at": output.share_expire_at,
            "has_password": enable_password
        }

    @staticmethod
    def update_project(
        db: Session,
        user_id: int,
        project_id: int,
        data: Dict[str, Any]
    ) -> VideoProject:
        """更新项目"""
        project = db.query(VideoProject).filter(
            VideoProject.id == project_id,
            VideoProject.user_id == user_id,
            VideoProject.deleted_at.is_(None)
        ).first()

        if not project:
            raise NotFoundException("项目不存在", code=40405)

        for key, value in data.items():
            if value is not None and hasattr(project, key):
                setattr(project, key, value)

        project.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete_project(db: Session, user_id: int, project_id: int) -> bool:
        """删除项目"""
        project = db.query(VideoProject).filter(
            VideoProject.id == project_id,
            VideoProject.user_id == user_id
        ).first()

        if project:
            project.deleted_at = datetime.utcnow()
            db.commit()
        return True


from datetime import timedelta