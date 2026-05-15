"""
统一响应 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List, Any
from datetime import datetime

T = TypeVar("T")


class BaseResponse(BaseModel):
    """基础响应"""
    code: int = Field(default=0, description="状态码: 0成功，其他失败")
    message: str = Field(default="success", description="消息")
    request_id: Optional[str] = Field(default=None, description="请求ID")
    timestamp: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()), description="时间戳")


class Response(BaseResponse, Generic[T]):
    """通用响应"""
    data: Optional[T] = Field(default=None, description="数据")


class PaginationInfo(BaseModel):
    """分页信息"""
    page: int = Field(..., description="当前页")
    page_size: int = Field(..., description="每页数量")
    total: int = Field(..., description="总数")
    total_pages: int = Field(..., description="总页数")
    has_next: bool = Field(..., description="是否有下一页")
    has_previous: bool = Field(..., description="是否有上一页")


class PaginatedData(BaseModel):
    """分页数据"""
    items: List[Any] = Field(default_factory=list, description="列表项")
    pagination: PaginationInfo = Field(..., description="分页信息")


class PaginatedResponse(BaseResponse):
    """列表响应"""
    data: Optional[PaginatedData] = Field(default=None, description="分页数据")


class ErrorDetail(BaseModel):
    """错误详情"""
    field: Optional[str] = None
    message: str


class ErrorResponse(BaseResponse):
    """错误响应"""
    code: int = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    errors: Optional[dict] = Field(default=None, description="字段错误")


def success_response(data: Any = None, message: str = "success") -> dict:
    """成功响应"""
    return {
        "code": 0,
        "message": message,
        "data": data,
        "timestamp": int(datetime.utcnow().timestamp())
    }


def error_response(code: int, message: str, errors: dict = None) -> dict:
    """错误响应"""
    return {
        "code": code,
        "message": message,
        "errors": errors,
        "timestamp": int(datetime.utcnow().timestamp())
    }