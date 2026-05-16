"""
数字人服务
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

from app.models.digital_human import DigitalHuman, DigitalHumanTask
from app.models.user import User
from app.core.exceptions import NotFoundException, ValidationException, QuotaExceededException


class DigitalHumanService:
    """数字人服务"""

    @staticmethod
    def get_list(
        db: Session,
        user_id: int,
        status: str = "all",
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取数字人列表"""
        query = db.query(DigitalHuman).filter(
            DigitalHuman.user_id == user_id,
            DigitalHuman.deleted_at.is_(None)
        )

        if status == "ready":
            query = query.filter(DigitalHuman.status == "completed")
        elif status == "processing":
            query = query.filter(DigitalHuman.status.in_(["pending", "processing"]))
        elif status == "failed":
            query = query.filter(DigitalHuman.status == "failed")

        total = query.count()
        items = query.order_by(
            DigitalHuman.created_at.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "items": [
                DigitalHumanService._format_item(db, dh)
                for dh in items
            ],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }

    @staticmethod
    def get_detail(db: Session, user_id: int, digital_human_id: int) -> Dict[str, Any]:
        """获取数字人详情"""
        dh = db.query(DigitalHuman).filter(
            DigitalHuman.id == digital_human_id,
            DigitalHuman.user_id == user_id,
            DigitalHuman.deleted_at.is_(None)
        ).first()

        if not dh:
            raise NotFoundException("数字人不存在", code=40402)

        return DigitalHumanService._format_detail(dh)

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """创建数字人"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("用户不存在")

        # 检查配额
        from app.services.wallet_service import WalletService
        quota = WalletService.calculate_quota(db, user)
        if quota["digital_human"]["remaining"] <= 0:
            raise QuotaExceededException("数字人配额已用完", code=30001)

        # 创建数字人
        dh = DigitalHuman(
            user_id=user_id,
            name=data["name"],
            description=data.get("description"),
            source_type=data.get("source_type", "single_photo"),
            source_photos=data.get("source_photos"),
            photo_count=len(data.get("source_photos", [])),
            authorization_type=data["authorization_type"],
            authorization_proof_url=data.get("authorization_proof_url"),
            authorization_expire_at=data.get("authorization_expire_at"),
            clothing_type=data.get("clothing_type"),
            background_type=data.get("background_type"),
            status="pending"
        )
        db.add(dh)
        db.flush()

        # 创建生成任务
        task = DigitalHumanTask(
            user_id=user_id,
            digital_human_id=dh.id,
            human_name=data["name"],
            task_type="create",
            status="queued",
            priority=5,
            model_provider="seeddance",
            model_name="digital_human_v2",
            input_config=data
        )
        db.add(task)
        db.commit()
        db.refresh(dh)

        return {
            "id": dh.id,
            "name": dh.name,
            "status": dh.status,
            "task_id": task.id,
            "estimated_seconds": 600
        }

    @staticmethod
    def update(
        db: Session,
        user_id: int,
        digital_human_id: int,
        data: Dict[str, Any]
    ) -> DigitalHuman:
        """更新数字人"""
        dh = db.query(DigitalHuman).filter(
            DigitalHuman.id == digital_human_id,
            DigitalHuman.user_id == user_id,
            DigitalHuman.deleted_at.is_(None)
        ).first()

        if not dh:
            raise NotFoundException("数字人不存在", code=40402)

        for key, value in data.items():
            if value is not None and hasattr(dh, key):
                setattr(dh, key, value)

        dh.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(dh)
        return dh

    @staticmethod
    def regenerate(
        db: Session,
        user_id: int,
        digital_human_id: int,
        new_photos: List[Dict]
    ) -> Dict[str, Any]:
        """重新生成数字人"""
        dh = db.query(DigitalHuman).filter(
            DigitalHuman.id == digital_human_id,
            DigitalHuman.user_id == user_id,
            DigitalHuman.deleted_at.is_(None)
        ).first()

        if not dh:
            raise NotFoundException("数字人不存在", code=40402)

        # 创建新版本
        dh.version_number += 1
        dh.parent_id = digital_human_id
        dh.status = "pending"
        dh.source_photos = new_photos
        dh.photo_count = len(new_photos)
        dh.error_message = None
        dh.retry_count = 0

        # 创建新任务
        task = DigitalHumanTask(
            user_id=user_id,
            digital_human_id=dh.id,
            human_name=dh.name,
            task_type="retrain",
            status="queued",
            priority=5,
            model_provider="seeddance",
            model_name="digital_human_v2",
            input_config={"new_photos": new_photos}
        )
        db.add(task)
        db.commit()
        db.refresh(dh)

        return {
            "task_id": task.id,
            "estimated_seconds": 600
        }

    @staticmethod
    def set_default(db: Session, user_id: int, digital_human_id: int) -> bool:
        """设置默认数字人"""
        # 取消其他默认
        db.query(DigitalHuman).filter(
            DigitalHuman.user_id == user_id,
            DigitalHuman.is_default == True
        ).update({"is_default": False})

        # 设置新的默认
        dh = db.query(DigitalHuman).filter(
            DigitalHuman.id == digital_human_id,
            DigitalHuman.user_id == user_id
        ).first()

        if dh:
            dh.is_default = True
            db.commit()
        return True

    @staticmethod
    def delete(db: Session, user_id: int, digital_human_id: int) -> bool:
        """删除数字人"""
        dh = db.query(DigitalHuman).filter(
            DigitalHuman.id == digital_human_id,
            DigitalHuman.user_id == user_id
        ).first()

        if dh:
            dh.deleted_at = datetime.utcnow()
            dh.status = "deleted"
            db.commit()
        return True

    @staticmethod
    def get_task(db: Session, user_id: int, task_id: int) -> Dict[str, Any]:
        """获取任务状态"""
        task = db.query(DigitalHumanTask).filter(
            DigitalHumanTask.id == task_id,
            DigitalHumanTask.user_id == user_id
        ).first()

        if not task:
            raise NotFoundException("任务不存在")

        return {
            "id": task.id,
            "task_type": task.task_type,
            "status": task.status,
            "progress": task.progress,
            "current_step": task.current_step,
            "estimated_seconds": 180 if task.status == "processing" else None,
            "started_at": task.started_at,
            "created_at": task.created_at
        }

    @staticmethod
    def check_photos(db: Session, user_id: int, photo_urls: List[str]) -> List[Dict[str, Any]]:
        """检查照片是否符合要求"""
        results = []
        for url in photo_urls:
            # TODO: 调用实际的图片检查服务
            # 目前返回模拟数据
            results.append({
                "url": url,
                "valid": True,
                "reason": None,
                "suggestion": None
            })
        return results

    @staticmethod
    def _format_item(db: Session, dh: DigitalHuman) -> Dict[str, Any]:
        """格式化列表项"""
        item = {
            "id": dh.id,
            "name": dh.name,
            "description": dh.description,
            "status": dh.status,
            "preview_image_url": dh.preview_image_url,
            "preview_video_url": dh.preview_video_url,
            "preview_video_duration": float(dh.preview_video_duration) if dh.preview_video_duration else None,
            "usage_count": dh.usage_count,
            "is_default": dh.is_default == True,
            "authorization_type": dh.authorization_type,
            "authorization_status": dh.authorization_status,
            "created_at": dh.created_at
        }

        # 如果正在处理中，获取任务进度
        if dh.status in ["pending", "processing"]:
            task = db.query(DigitalHumanTask).filter(
                DigitalHumanTask.digital_human_id == dh.id
            ).order_by(DigitalHumanTask.created_at.desc()).first()
            if task:
                item["progress"] = task.progress

        return item

    @staticmethod
    def _format_detail(dh: DigitalHuman) -> Dict[str, Any]:
        """格式化详情"""
        return {
            "id": dh.id,
            "user_id": dh.user_id,
            "name": dh.name,
            "description": dh.description,
            "source_type": dh.source_type,
            "source_photos": dh.source_photos,
            "photo_count": dh.photo_count,
            "gender": dh.gender,
            "age_group": dh.age_group,
            "clothing_type": dh.clothing_type,
            "background_type": dh.background_type,
            "status": dh.status,
            "preview_image_url": dh.preview_image_url,
            "preview_video_url": dh.preview_video_url,
            "usage_count": dh.usage_count,
            "is_default": dh.is_default == True,
            "authorization_type": dh.authorization_type,
            "authorization_status": dh.authorization_status,
            "version_number": dh.version_number,
            "created_at": dh.created_at,
            "updated_at": dh.updated_at
        }