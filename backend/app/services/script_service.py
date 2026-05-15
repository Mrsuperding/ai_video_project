"""
脚本服务
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.script import Script, ScriptTemplate, AIWritingTask
from app.core.exceptions import NotFoundException, ValidationException


class ScriptService:
    """脚本服务"""

    @staticmethod
    def get_list(
        db: Session,
        user_id: int,
        status: str = "all",
        category: str = None,
        keyword: str = None,
        is_template: bool = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取脚本列表"""
        query = db.query(Script).filter(
            Script.user_id == user_id,
            Script.deleted_at.is_(None)
        )

        if status and status != "all":
            query = query.filter(Script.status == status)

        if category:
            query = query.filter(Script.category == category)

        if keyword:
            query = query.filter(Script.title.like(f"%{keyword}%"))

        if is_template is not None:
            query = query.filter(Script.is_template == ("1" if is_template else "0"))

        total = query.count()
        items = query.order_by(
            Script.created_at.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "items": [
                {
                    "id": s.id,
                    "title": s.title,
                    "description": s.description,
                    "word_count": s.word_count,
                    "estimated_duration": float(s.estimated_duration) if s.estimated_duration else None,
                    "language": s.language,
                    "category": s.category,
                    "tags": s.tags,
                    "status": s.status,
                    "usage_count": s.usage_count,
                    "created_at": s.created_at
                }
                for s in items
            ],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }

    @staticmethod
    def get_detail(db: Session, user_id: int, script_id: int) -> Dict[str, Any]:
        """获取脚本详情"""
        script = db.query(Script).filter(
            Script.id == script_id,
            Script.user_id == user_id,
            Script.deleted_at.is_(None)
        ).first()

        if not script:
            raise NotFoundException("脚本不存在", code=40403)

        return {
            "id": script.id,
            "title": script.title,
            "description": script.description,
            "content": script.content,
            "word_count": script.word_count,
            "estimated_duration": float(script.estimated_duration) if script.estimated_duration else None,
            "language": script.language,
            "voice_id": script.voice_id,
            "base_tts_speed": float(script.base_tts_speed) if script.base_tts_speed else 1.0,
            "category": script.category,
            "tags": script.tags,
            "status": script.status,
            "created_at": script.created_at,
            "updated_at": script.updated_at
        }

    @staticmethod
    def create(db: Session, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建脚本"""
        content = data.get("content", {})
        segments = content.get("segments", [])

        # 计算字数和预估时长
        plain_text = "".join([seg.get("text", "") for seg in segments])
        word_count = len(plain_text)
        estimated_duration = sum([seg.get("duration", 3) for seg in segments])

        script = Script(
            user_id=user_id,
            title=data["title"],
            description=data.get("description"),
            content=content,
            plain_text=plain_text,
            word_count=word_count,
            estimated_duration=estimated_duration,
            language=data.get("language", "zh"),
            category=data.get("category"),
            tags=data.get("tags"),
            status="draft"
        )
        db.add(script)
        db.commit()
        db.refresh(script)

        return {
            "id": script.id,
            "title": script.title,
            "word_count": script.word_count,
            "estimated_duration": float(script.estimated_duration),
            "status": script.status
        }

    @staticmethod
    def update(db: Session, user_id: int, script_id: int, data: Dict[str, Any]) -> Script:
        """更新脚本"""
        script = db.query(Script).filter(
            Script.id == script_id,
            Script.user_id == user_id,
            Script.deleted_at.is_(None)
        ).first()

        if not script:
            raise NotFoundException("脚本不存在", code=40403)

        for key, value in data.items():
            if key == "content" and value:
                segments = value.get("segments", [])
                script.plain_text = "".join([seg.get("text", "") for seg in segments])
                script.word_count = len(script.plain_text)
                script.estimated_duration = sum([seg.get("duration", 3) for seg in segments])

            if value is not None and hasattr(script, key):
                setattr(script, key, value)

        script.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(script)
        return script

    @staticmethod
    def delete(db: Session, user_id: int, script_id: int) -> bool:
        """删除脚本"""
        script = db.query(Script).filter(
            Script.id == script_id,
            Script.user_id == user_id
        ).first()

        if script:
            script.deleted_at = datetime.utcnow()
            db.commit()
        return True

    @staticmethod
    def save_as_template(
        db: Session,
        user_id: int,
        script_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """保存为模板"""
        script = db.query(Script).filter(
            Script.id == script_id,
            Script.user_id == user_id
        ).first()

        if not script:
            raise NotFoundException("脚本不存在", code=40403)

        template = ScriptTemplate(
            name=data["name"],
            description=data.get("description"),
            category=data.get("category", script.category),
            content=script.content,
            source="user",
            creator_id=user_id
        )
        db.add(template)
        db.commit()
        db.refresh(template)

        return {"id": template.id, "name": template.name}

    @staticmethod
    def get_templates(
        db: Session,
        category: str = None,
        source: str = "platform",
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取模板列表"""
        query = db.query(ScriptTemplate).filter(ScriptTemplate.status == "active")

        if category:
            query = query.filter(ScriptTemplate.category == category)

        if source:
            query = query.filter(ScriptTemplate.source == source)

        total = query.count()
        items = query.order_by(
            ScriptTemplate.usage_count.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "items": [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description,
                    "cover_image_url": t.cover_image_url,
                    "category": t.category,
                    "tags": t.tags,
                    "input_fields": t.input_fields,
                    "usage_count": t.usage_count,
                    "rating": float(t.rating) if t.rating else None,
                    "created_at": t.created_at
                }
                for t in items
            ],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }

    @staticmethod
    def get_template_detail(db: Session, template_id: int) -> Dict[str, Any]:
        """获取模板详情"""
        template = db.query(ScriptTemplate).filter(
            ScriptTemplate.id == template_id,
            ScriptTemplate.status == "active"
        ).first()

        if not template:
            raise NotFoundException("模板不存在")

        return {
            "id": template.id,
            "name": template.name,
            "description": template.description,
            "prompt_template": template.prompt_template,
            "example_text": template.example_text,
            "category": template.category,
            "input_fields": template.input_fields or [],
            "usage_count": template.usage_count,
            "rating": float(template.rating) if template.rating else None,
            "rating_count": template.rating_count
        }

    @staticmethod
    def ai_generate(
        db: Session,
        user_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """AI生成文案"""
        task = AIWritingTask(
            user_id=user_id,
            task_type="generate",
            status="queued",
            input_prompt=data.get("input_prompt"),
            template_id=data.get("template_id"),
            style=data.get("style", "professional"),
            emotion=data.get("emotion", "neutral"),
            target_language=data.get("target_language", "zh")
        )
        db.add(task)
        db.commit()

        # TODO: 实际调用AI服务
        output_text = "AI生成的文案内容..."
        output_segments = [{"text": output_text, "duration": 5, "speed": 1.0, "emotion": "neutral"}]

        task.status = "completed"
        task.progress = 100
        task.output_text = output_text
        task.output_segments = output_segments
        task.output_tokens = 200
        task.cost_cents = 1
        db.commit()

        # 创建脚本
        script = Script(
            user_id=user_id,
            title="AI生成脚本",
            content={"segments": output_segments},
            plain_text=output_text,
            word_count=len(output_text),
            estimated_duration=5,
            ai_generated="1",
            ai_prompt=data.get("input_prompt"),
            status="draft"
        )
        db.add(script)
        db.commit()
        db.refresh(script)

        return {
            "task_id": task.id,
            "script_id": script.id,
            "content": {
                "plain_text": output_text,
                "segments": output_segments
            },
            "word_count": len(output_text),
            "estimated_duration": 5
        }

    @staticmethod
    def ai_rewrite(
        db: Session,
        user_id: int,
        text: str,
        task_type: str,
        style: str = "professional",
        target_language: str = "zh"
    ) -> Dict[str, Any]:
        """AI改写/润色"""
        task = AIWritingTask(
            user_id=user_id,
            task_type=task_type,
            status="queued",
            input_text=text,
            style=style,
            target_language=target_language
        )
        db.add(task)
        db.commit()

        # TODO: 实际调用AI服务
        output_text = f"改写后的文本: {text}"
        output_segments = [{"text": output_text, "duration": 5, "speed": 1.0, "emotion": "neutral"}]

        task.status = "completed"
        task.progress = 100
        task.output_text = output_text
        task.output_segments = output_segments
        task.output_tokens = 100
        task.cost_cents = 1
        db.commit()

        return {
            "task_id": task.id,
            "result": {
                "text": output_text,
                "segments": output_segments
            }
        }

    @staticmethod
    def get_ai_task(db: Session, user_id: int, task_id: int) -> Dict[str, Any]:
        """获取AI任务状态"""
        task = db.query(AIWritingTask).filter(
            AIWritingTask.id == task_id,
            AIWritingTask.user_id == user_id
        ).first()

        if not task:
            raise NotFoundException("任务不存在")

        return {
            "id": task.id,
            "task_type": task.task_type,
            "status": task.status,
            "progress": task.progress,
            "result": {
                "text": task.output_text,
                "segments": task.output_segments
            } if task.output_text else None,
            "input_tokens": task.input_tokens,
            "output_tokens": task.output_tokens,
            "cost_cents": task.cost_cents
        }