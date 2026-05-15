"""
自定义异常
"""
from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class AppException(HTTPException):
    """应用异常基类"""

    def __init__(
        self,
        status_code: int,
        code: int,
        message: str,
        headers: Optional[Dict[str, str]] = None,
        errors: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        self.errors = errors
        super().__init__(
            status_code=status_code,
            detail={
                "code": code,
                "message": message,
                "errors": errors
            },
            headers=headers
        )


class UnauthorizedException(AppException):
    """未认证异常"""

    def __init__(self, message: str = "Unauthorized", code: int = 20001):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=code,
            message=message
        )


class ForbiddenException(AppException):
    """禁止访问异常"""

    def __init__(self, message: str = "Permission denied", code: int = 20004):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code=code,
            message=message
        )


class NotFoundException(AppException):
    """资源不存在异常"""

    def __init__(self, message: str = "Resource not found", code: int = 40401):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code=code,
            message=message
        )


class ValidationException(AppException):
    """参数验证异常"""

    def __init__(self, message: str = "Invalid parameter", errors: Optional[Dict] = None, code: int = 40001):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code=code,
            message=message,
            errors=errors
        )


class QuotaExceededException(AppException):
    """配额不足异常"""

    def __init__(self, message: str = "Quota exceeded", code: int = 30001):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code=code,
            message=message
        )


class ConflictException(AppException):
    """资源冲突异常"""

    def __init__(self, message: str = "Resource conflict", code: int = 40901):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code=code,
            message=message
        )