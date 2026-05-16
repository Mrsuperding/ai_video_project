"""
AI写作 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.script import AIGenerateRequest, AIRewriteRequest
from app.schemas.response import success_response, error_response
from app.services.script_service import ScriptService

router = APIRouter()


@router.post("/generate")
def ai_generate(
    request: AIGenerateRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """AI生成文案"""
    try:
        data = request.model_dump()
        result = ScriptService.ai_generate(db, user_id, data)
        return success_response(result, message="生成成功")
    except Exception as e:
        return error_response(50001, str(e))


@router.post("/rewrite")
def ai_rewrite(
    request: AIRewriteRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """AI改写/润色"""
    try:
        result = ScriptService.ai_rewrite(
            db, user_id, request.text, request.task_type,
            request.style, request.target_language
        )
        return success_response(result)
    except Exception as e:
        return error_response(50001, str(e))


@router.get("/tasks/{task_id}")
def get_ai_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取AI任务状态"""
    try:
        task = ScriptService.get_ai_task(db, user_id, task_id)
        return success_response(task)
    except NotFoundException as e:
        return error_response(e.code, e.message)