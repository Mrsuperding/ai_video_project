"""
脚本 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas.script import *
from app.schemas.response import success_response, error_response
from app.services.script_service import ScriptService
from app.core.exceptions import NotFoundException

router = APIRouter()


@router.get("")
async def get_list(
    status: str = "all",
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    is_template: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取脚本列表"""
    result = ScriptService.get_list(
        db, user_id, status, category, keyword, is_template, page, page_size
    )
    return success_response(result)


@router.get("/{script_id}")
async def get_detail(
    script_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取脚本详情"""
    try:
        detail = ScriptService.get_detail(db, user_id, script_id)
        return success_response(detail)
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.post("")
async def create(
    request: CreateScriptRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """创建脚本"""
    try:
        data = request.model_dump()
        if data.get("content") and isinstance(data["content"], dict):
            pass  # content already a dict, no conversion needed
        elif request.content and hasattr(request.content, 'model_dump'):
            data["content"] = request.content.model_dump()
        result = ScriptService.create(db, user_id, data)
        return success_response(result, message="创建成功")
    except Exception as e:
        return error_response(50001, str(e))


@router.patch("/{script_id}")
async def update(
    script_id: int,
    request: UpdateScriptRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """更新脚本"""
    try:
        data = request.model_dump(exclude_unset=True)
        if request.content:
            data["content"] = request.content.model_dump()
        script = ScriptService.update(db, user_id, script_id, data)
        return success_response({
            "id": script.id,
            "title": script.title
        })
    except NotFoundException as e:
        return error_response(e.code, e.message)


@router.delete("/{script_id}")
async def delete(
    script_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """删除脚本"""
    ScriptService.delete(db, user_id, script_id)
    return success_response(message="删除成功")


@router.post("/{script_id}/save-as-template")
async def save_as_template(
    script_id: int,
    request: SaveAsTemplateRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """保存为模板"""
    try:
        data = request.model_dump()
        result = ScriptService.save_as_template(db, user_id, script_id, data)
        return success_response(result)
    except NotFoundException as e:
        return error_response(e.code, e.message)


# AI 写作
@router.post("/generate")
async def ai_generate(
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
async def ai_rewrite(
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
async def get_ai_task(
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


# 脚本模板
@router.get("/template/list")
async def get_templates(
    category: Optional[str] = None,
    source: str = "platform",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取模板列表"""
    result = ScriptService.get_templates(db, category, source, page, page_size)
    return success_response(result)


@router.get("/template/{template_id}")
async def get_template_detail(
    template_id: int,
    db: Session = Depends(get_db)
):
    """获取模板详情"""
    try:
        detail = ScriptService.get_template_detail(db, template_id)
        return success_response(detail)
    except NotFoundException as e:
        return error_response(e.code, e.message)