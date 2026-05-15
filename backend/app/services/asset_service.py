"""
素材服务
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

from app.models.asset import UserAsset, PlatformAsset, AssetCategory
from app.core.exceptions import NotFoundException


class AssetService:
    """素材服务"""

    @staticmethod
    def get_user_assets(
        db: Session,
        user_id: int,
        asset_type: str = None,
        category: str = None,
        tag: str = None,
        keyword: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取用户素材列表"""
        query = db.query(UserAsset).filter(
            UserAsset.user_id == user_id,
            UserAsset.deleted_at.is_(None)
        )

        if asset_type:
            query = query.filter(UserAsset.asset_type == asset_type)

        if category:
            query = query.filter(UserAsset.category == category)

        if keyword:
            query = query.filter(UserAsset.name.like(f"%{keyword}%"))

        total = query.count()
        items = query.order_by(
            UserAsset.created_at.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "items": [
                {
                    "id": a.id,
                    "name": a.name,
                    "asset_type": a.asset_type,
                    "file_url": a.file_url,
                    "thumbnail_url": a.file_url,
                    "width": a.width,
                    "height": a.height,
                    "file_size": a.file_size,
                    "category": a.category,
                    "tags": a.tags,
                    "usage_count": a.usage_count,
                    "created_at": a.created_at
                }
                for a in items
            ],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }

    @staticmethod
    def get_upload_token(
        db: Session,
        user_id: int,
        file_name: str,
        file_size: int,
        asset_type: str
    ) -> Dict[str, Any]:
        """获取上传凭证"""
        # TODO: 调用OSS获取上传凭证
        token = f"token_{uuid.uuid4().hex}"
        return {
            "upload_url": "https://oss.example.com/upload",
            "upload_token": token,
            "asset_id": 0,  # 创建素材后返回真实ID
            "expire_seconds": 3600
        }

    @staticmethod
    def confirm_upload(
        db: Session,
        user_id: int,
        asset_id: int,
        data: Dict[str, Any]
    ) -> UserAsset:
        """确认上传完成"""
        asset = db.query(UserAsset).filter(
            UserAsset.id == asset_id,
            UserAsset.user_id == user_id
        ).first()

        if not asset:
            raise NotFoundException("素材不存在", code=40404)

        asset.name = data.get("name", asset.name)
        asset.category = data.get("category", asset.category)
        asset.tags = data.get("tags", asset.tags)
        asset.status = "ready"

        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def update_asset(
        db: Session,
        user_id: int,
        asset_id: int,
        data: Dict[str, Any]
    ) -> UserAsset:
        """更新素材"""
        asset = db.query(UserAsset).filter(
            UserAsset.id == asset_id,
            UserAsset.user_id == user_id,
            UserAsset.deleted_at.is_(None)
        ).first()

        if not asset:
            raise NotFoundException("素材不存在", code=40404)

        for key, value in data.items():
            if value is not None and hasattr(asset, key):
                setattr(asset, key, value)

        asset.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def delete_asset(db: Session, user_id: int, asset_id: int) -> bool:
        """删除素材"""
        asset = db.query(UserAsset).filter(
            UserAsset.id == asset_id,
            UserAsset.user_id == user_id
        ).first()

        if asset:
            asset.deleted_at = datetime.utcnow()
            db.commit()
        return True

    @staticmethod
    def get_platform_assets(
        db: Session,
        asset_type: str = None,
        category: str = None,
        license_type: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取平台素材列表"""
        query = db.query(PlatformAsset).filter(PlatformAsset.status == "active")

        if asset_type:
            query = query.filter(PlatformAsset.asset_type == asset_type)

        if category:
            query = query.filter(PlatformAsset.category == category)

        if license_type:
            query = query.filter(PlatformAsset.license_type == license_type)

        total = query.count()
        items = query.order_by(
            PlatformAsset.usage_count.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "items": [
                {
                    "id": a.id,
                    "asset_type": a.asset_type,
                    "file_url": a.file_url,
                    "thumbnail_url": a.file_url,
                    "width": a.width,
                    "height": a.height,
                    "category": a.category,
                    "license_type": a.license_type,
                    "membership_required": a.membership_required,
                    "usage_count": a.usage_count
                }
                for a in items
            ],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }

    @staticmethod
    def get_categories(
        db: Session,
        asset_type: str = None
    ) -> List[Dict[str, Any]]:
        """获取素材分类"""
        query = db.query(AssetCategory).filter(
            AssetCategory.status == "active",
            AssetCategory.parent_id.is_(None)
        )

        if asset_type:
            query = query.filter(
                AssetCategory.asset_types.contains(asset_type)
            )

        categories = query.order_by(AssetCategory.sort_order).all()

        result = []
        for cat in categories:
            item = {
                "id": cat.id,
                "name": cat.name,
                "subcategories": []
            }

            subcats = db.query(AssetCategory).filter(
                AssetCategory.parent_id == cat.id,
                AssetCategory.status == "active"
            ).order_by(AssetCategory.sort_order).all()

            for sub in subcats:
                item["subcategories"].append({
                    "id": sub.id,
                    "name": sub.name
                })

            result.append(item)

        return result