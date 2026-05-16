"""
语音服务
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

from app.models.voice import VoiceClone
from app.core.exceptions import NotFoundException


class VoiceService:
    """声音克隆服务"""

    @staticmethod
    def get_list(
        db: Session,
        user_id: int,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取声音克隆列表"""
        query = db.query(VoiceClone).filter(VoiceClone.user_id == user_id)

        total = query.count()
        items = query.order_by(
            VoiceClone.created_at.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "items": [
                {
                    "id": v.id,
                    "name": v.name,
                    "gender": v.gender,
                    "age_group": v.age_group,
                    "status": v.status,
                    "sample_audio_url": v.sample_audio_url,
                    "duration": float(v.source_duration) if v.source_duration else None,
                    "usage_count": v.usage_count,
                    "is_default": v.is_default == True,
                    "created_at": v.created_at
                }
                for v in items
            ],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """创建声音克隆"""
        voice = VoiceClone(
            user_id=user_id,
            digital_human_id=data.get("digital_human_id"),
            name=data["name"],
            source_audio_url=data["source_audio_url"],
            language=data.get("language", "zh"),
            emotion=data.get("emotion", "neutral"),
            status="pending"
        )
        db.add(voice)
        db.commit()

        return {
            "id": voice.id,
            "status": voice.status,
            "task_id": voice.id,
            "estimated_seconds": 300
        }

    @staticmethod
    def preview_tts(
        db: Session,
        user_id: int,
        text: str,
        voice_id: Optional[int] = None,
        config: Optional[dict] = None
    ) -> Dict[str, Any]:
        """TTS 预览"""
        voice = None
        if voice_id:
            voice = db.query(VoiceClone).filter(
                VoiceClone.id == voice_id,
                VoiceClone.user_id == user_id
            ).first()
            if not voice:
                raise NotFoundException("音色不存在", code=40403)

        # TODO: 调用实际的 TTS 服务
        # 目前返回模拟数据
        return {
            "audio_url": "https://cdn.example.com/preview/tts_sample.mp3",
            "duration": len(text) / 5.0,  # 估算
            "text_length": len(text),
            "voice_id": voice_id,
            "voice_name": voice.name if voice else None
        }

    @staticmethod
    def set_default(db: Session, user_id: int, voice_id: int) -> bool:
        """设置默认音色"""
        db.query(VoiceClone).filter(
            VoiceClone.user_id == user_id,
            VoiceClone.is_default == True
        ).update({"is_default": False})

        voice = db.query(VoiceClone).filter(
            VoiceClone.id == voice_id,
            VoiceClone.user_id == user_id
        ).first()

        if voice:
            voice.is_default = True
            db.commit()
        return True

    @staticmethod
    def delete(db: Session, user_id: int, voice_id: int) -> bool:
        """删除声音克隆"""
        voice = db.query(VoiceClone).filter(
            VoiceClone.id == voice_id,
            VoiceClone.user_id == user_id
        ).first()

        if voice:
            db.delete(voice)
            db.commit()
        return True