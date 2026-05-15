"""
限流器
"""
import time
from typing import Dict, Optional, Callable
from fastapi import Request, HTTPException, status
from app.redis import get_redis


class RateLimiter:
    """基于 Redis 的限流器"""

    def __init__(self, key_prefix: str, limit: int, window: int):
        """
        Args:
            key_prefix: 限流 key 前缀
            limit: 限制次数
            window: 时间窗口(秒)
        """
        self.key_prefix = key_prefix
        self.limit = limit
        self.window = window

    async def is_allowed(self, identifier: str) -> bool:
        """检查是否允许请求"""
        redis = await get_redis()
        key = f"{self.key_prefix}:{identifier}"

        # 使用滑动窗口算法
        now = time.time()
        window_start = now - self.window

        # 移除窗口外的记录
        await redis.zremrangebyscore(key, 0, window_start)

        # 获取当前请求数
        current_count = await redis.zcard(key)

        if current_count >= self.limit:
            return False

        # 添加当前请求
        await redis.zadd(key, {str(now): now})
        await redis.expire(key, self.window)

        return True

    async def get_retry_after(self, identifier: str) -> int:
        """获取重试等待时间(秒)"""
        redis = await get_redis()
        key = f"{self.key_prefix}:{identifier}"

        oldest = await redis.zrange(key, 0, 0, withscores=True)
        if oldest:
            oldest_time = oldest[0][1]
            retry_after = int(oldest_time + self.window - time.time())
            return max(1, retry_after)
        return 1


# 预定义的限流器
login_limiter = RateLimiter("rate_limit:login", limit=3, window=60)  # 每IP每分钟3次
sms_limiter = RateLimiter("rate_limit:sms", limit=1, window=300)  # 每手机号每5分钟1次
upload_limiter = RateLimiter("rate_limit:upload", limit=10, window=60)  # 每用户每分钟10次
api_limiter = RateLimiter("rate_limit:api", limit=100, window=60)  # 每用户每分钟100次


async def check_rate_limit(limiter: RateLimiter, identifier: str):
    """检查限流并抛出异常"""
    if not await limiter.is_allowed(identifier):
        retry_after = await limiter.get_retry_after(identifier)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "code": 42901,
                "message": "Rate limit exceeded",
                "retry_after": retry_after
            },
            headers={"Retry-After": str(retry_after)}
        )